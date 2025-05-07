import copy

from .exceptions import AccessDeniedError, DecryptionError, PipelineDesializationError
from .utils.de_serialization import deserialize, serialize
from .utils.logging import log_error, log_pipeline_results
from .utils.misc import get_encryption_key, lazy_import


class Pipeline:
    """
    Represents a Redis pipeline wrapper tailored for the redisimnest key management system.

    This class supports metadata tracking for each pipelined command, enabling structured 
    deserialization, secret/password decryption, TTL auto-renewal, and pretty logging of results.
    Intended for internal use by cluster and key abstractions to coordinate bulk Redis operations
    while preserving rich context.
    """
    def __init__(self, redis):
        """
        Initialize a new redisimnest pipeline.

        Args:
            redis: The raw aioredis Redis connection or client.
        """
        self.redis = redis
        self.pipe = redis.pipeline()
        self._metas = []  # must be populated when attaching keys


    
    def add(self, method_call, *args, **kwargs):
        """
        Adds a key method call to the pipeline with associated metadata.

        Args:
            method_call: A method call from a Key class instance that performs Redis operations.
                        For example, `root.user(123).first_name.set(25)`.

        Returns:
            The result of the key method call (for chaining purposes).
        """
        # Extract method and arguments
        method_name = method_call.__name__
        key_instance = method_call.__self__  # The instance of the key
        key = key_instance.key
        
        if not isinstance(args, tuple):
            raise TypeError(f"args that passed to key are invalid. expected args to be tuple, but got {type(args)}")
        if not isinstance(kwargs, dict):
            raise TypeError(f"kwargs that passed to key are invalid. expected kwargs to be dict, but got {type(kwargs)}")

        reveal = kwargs.pop('reveal', None)

        # Create command metadata
        command_meta = {
            'is_password': key_instance.is_password,
            'is_secret': key_instance.is_secret,
            'method': method_name,
            'key_id': id(key_instance),
            'key': key_instance.key,
            'default_value': copy.deepcopy(key_instance.default_value),
            'reveal': reveal,
            'ttl': getattr(key_instance, 'the_ttl', None),
            'name': getattr(key_instance, '_name', "???"),
            'args': args,
            'kwargs': kwargs
        }

        # Add the command metadata to the pipeline's list of metas
        self._metas.append(command_meta)

        # Serialize value if the method is 'set'
        if method_name == 'set':
            val = args[0]  # Assuming the first argument is the value

            val = getattr(key_instance, '_resolve_value')(val)
            val = serialize(val)  # Serialize the value

            args = (val,) + args[1:]  # Replace value in args

            # Resolve TTL (ex) from kwargs, args, or key_instance
            ex = kwargs.get('ex') or (args[1] if len(args) >= 2 else None)
            the_ttl = getattr(key_instance, 'the_ttl', None)  # Safely get ttl
            if the_ttl is not None:
                ex = ex or the_ttl
            
            # Update args or kwargs with resolved TTL (ex)
            if len(args) >= 2:
                args = args[:1] + (ex,) + args[2:]
            else:
                kwargs['ex'] = ex
        
        return getattr(self.pipe, method_name)(key, *args, **kwargs)
    

    async def execute(self):
        """
        Execute all commands queued in the pipeline, with deserialization and post-processing.

        Deserializes GET results, decrypts secrets or passwords when permitted, applies TTL
        auto-renewal for eligible keys, and logs all outputs using a structured format.

        Returns:
            list: The final processed results from each pipelined command, in order.
                Returns raw Redis results if deserialization fails due to mismatched metadata.
        
        Raises:
            AccessDeniedError: If a password-protected key is accessed without permission.
        """

        results = await self.pipe.execute()

        if len(results) != len(self._metas):
            log_error(str(PipelineDesializationError("Could not deserialize pipeline results. (lengths of metas and results do not match!)")))

            log_pipeline_results(
                pipe_id=id(self),
                result_metas=self._metas,
                results=results
            )
            return results
        processed_results = await self._post_process_results(results)
        return processed_results
    
    async def _post_process_results(self, results) -> list:
        deserialized_results = []
        for meta, result in zip(self._metas, results):
            method = meta.get('method')
            key = meta.get('key')

            if method == 'get':
                result = copy.deepcopy(result)

                if result is None:
                    deserialized_results.append(meta.get('default_value'))
                    continue

                result = deserialize(result)
                if result is None:
                    deserialized_results.append(None)
                    continue

                if meta.get('is_secret'):
                    try:
                        ENCRYPTION_KEY = get_encryption_key()
                        fernet = lazy_import('cryptography').fernet.Fernet(ENCRYPTION_KEY)
                        result = fernet.decrypt(result.encode()).decode()
                    except Exception as e:
                        log_error(str(DecryptionError(str(e))))
                        result = "[decryption-error]"

                if meta.get('is_password'):
                    if meta.get('reveal'):
                        deserialized_results.append(result)
                    else:
                        raise AccessDeniedError("To access secrets, set ALLOW_SECRET_ACCESS=1.")
                else:
                    deserialized_results.append(result)

                if meta.get('ttl') is not None and getattr(self, 'ttl_auto_renew', False):
                    await self.redis.expire(key, meta['ttl'])

            else:
                # Non-GET method (set, delete, etc.)
                deserialized_results.append(result)

        log_pipeline_results(
            pipe_id=id(self),
            result_metas=self._metas,
            results=deserialized_results
        )
        return deserialized_results