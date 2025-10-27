from flask_openapi3 import APIBlueprint, Tag

health_tag = Tag(name="Health", description="Health check operations")

api_v1_health = APIBlueprint('health', __name__, url_prefix='/v1')


@api_v1_health.get(
    '/ping',
    tags=[health_tag]
)
def ping():
    """
    Ping endpoint (v1)
    ---
    Returns a JSON object with a pong message.
    Useful for health checks and connectivity tests.
    """
    return {"msg": "pong"}, 200
