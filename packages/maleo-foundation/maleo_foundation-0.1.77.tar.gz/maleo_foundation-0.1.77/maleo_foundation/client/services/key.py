from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from maleo_foundation.expanded_types.key import BaseKeyResultsTypes
from maleo_foundation.managers.client.base import ClientService
from maleo_foundation.models.transfers.general.key import BaseKeyGeneralTransfers
from maleo_foundation.models.transfers.parameters.key import BaseKeyParametersTransfers
from maleo_foundation.models.transfers.results.key import BaseKeyResultsTransfers
from maleo_foundation.utils.exceptions import BaseExceptions

class MaleoFoundationKeyClientService(ClientService):
    def create_private(self, parameters:BaseKeyParametersTransfers.CreatePrivateOrPair) -> BaseKeyResultsTypes.CreatePrivate:
        """Create an RSA private key with X.509 encoding in .pem format."""
        @BaseExceptions.service_exception_handler(
            operation="creating private key",
            logger=self._logger,
            fail_result_class=BaseKeyResultsTransfers.Fail
        )
        def _impl():
            #* Create private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=parameters.key_size,
                backend=default_backend()
            )

            if parameters.password is None:
                encryption_algorithm = serialization.NoEncryption()
            else:
                encryption_algorithm = serialization.BestAvailableEncryption(parameters.password.encode())

            #* Serialize private key to PEM format
            private_key_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=encryption_algorithm
            )

            self._logger.info("Successfully created private key")
            data = BaseKeyGeneralTransfers.PrivateKey(value=private_key_bytes.decode())
            return BaseKeyResultsTransfers.CreatePrivate(data=data)
        return _impl()

    def create_public(self, parameters:BaseKeyParametersTransfers.CreatePublic) -> BaseKeyResultsTypes.CreatePublic:
        """Create an RSA public key with X.509 encoding in .pem format."""
        @BaseExceptions.service_exception_handler(
            operation="creating public key",
            logger=self._logger,
            fail_result_class=BaseKeyResultsTransfers.Fail
        )
        def _impl():
            #* Serialize private key
            private_key_bytes = parameters.value.encode()
            private_key = serialization.load_pem_private_key(
                private_key_bytes,
                password=parameters.password.encode() if parameters.password else None,
                backend=default_backend()
            )

            public_key = private_key.public_key() #* Create public key

            #* Serialize public key to PEM format
            public_key_bytes = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            self._logger.info("Successfully created public key")
            data = BaseKeyGeneralTransfers.PublicKey(value=public_key_bytes.decode())
            return BaseKeyResultsTransfers.CreatePublic(data=data)
        return _impl()

    def create_pair(self, parameters:BaseKeyParametersTransfers.CreatePrivateOrPair) -> BaseKeyResultsTypes.CreatePair:
        """Create an RSA key pair with X.509 encoding in .pem format."""
        @BaseExceptions.service_exception_handler(
            operation="creating key pair",
            logger=self._logger,
            fail_result_class=BaseKeyResultsTransfers.Fail
        )
        def _impl():
            #* Create private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=parameters.key_size,
                backend=default_backend()
            )

            if parameters.password is None:
                encryption_algorithm = serialization.NoEncryption()
            else:
                encryption_algorithm = serialization.BestAvailableEncryption(parameters.password.encode())

            #* Serialize private key to PEM format
            private_key_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=encryption_algorithm
            )
            private = BaseKeyGeneralTransfers.PrivateKey(value=private_key_bytes.decode())

            public_key = private_key.public_key() #* Create public key

            #* Serialize public key to PEM format
            public_key_bytes = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            public = BaseKeyGeneralTransfers.PublicKey(value=public_key_bytes.decode())

            self._logger.info("Successfully created key pair")
            data = BaseKeyGeneralTransfers.KeyPair(private=private, public=public)
            return BaseKeyResultsTransfers.CreatePair(data=data)
        return _impl()