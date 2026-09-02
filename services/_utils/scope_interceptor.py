from app_settings import JWT_SIGN_KEY, JWT_ALG
import jwt, grpc



def create_error_message(code: grpc.StatusCode, details: str):
    return grpc.unary_unary_rpc_method_handler(lambda r, ctx: ctx.abort(code, details))


class ScopeInterceptor(grpc.ServerInterceptor):

    JWT_TOKEN = "authorization"

    # rewrite to take JWT TOKENS
    def intercept_service(self, continuation, handler_call_details):
        jwt_token= self.__extract_jwt_from_meta(handler_call_details.invocation_metadata)
        replaced_path = self.__replace_path(handler_call_details.method)

        try:
            jwt_data = jwt.decode(
                jwt=jwt_token,
                key=JWT_SIGN_KEY,
                algorithms=JWT_ALG
            )
        except jwt.ExpiredSignatureError:
            return create_error_message(
                code=grpc.StatusCode.UNAUTHENTICATED,
                details="The token has been expired"
            )
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return create_error_message(
                code=grpc.StatusCode.UNAUTHENTICATED,
                details="Invalid token"
            )
        
        user_scopes = jwt_data.get("scopes")

        if user_scopes is None:
            return create_error_message(
                details="The token structure is invalid",
                code=grpc.StatusCode.UNAUTHENTICATED
            )

        if replaced_path in user_scopes:
            return continuation(handler_call_details)

        return create_error_message(
            details="You don't have permissions to this services",
            code=grpc.StatusCode.PERMISSION_DENIED
        )

    def __extract_jwt_from_meta(self, metadata) -> str:
        for meta in metadata:
            if meta.key == self.JWT_TOKEN:
                return meta.value
        return None

    def __replace_path(self, path: str) -> str:
        return path.lower().replace("/", ".")[1:]


# 0, 30
# 5, 10
# 38, 40 
# output: 2 rooms required