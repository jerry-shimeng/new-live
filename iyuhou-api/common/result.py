def of(d: object) -> dict:
	return {'code': 0, 'data': d, 'message': ''}


def success() -> dict:
	return {'code': 0, 'data': {}, 'message': ''}


def fail(code: int = -1, message: str = 'error') -> dict:
	return {'code': code, 'message': message, 'data': {}}
