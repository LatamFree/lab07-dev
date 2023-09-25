from jsonschema import validate, exceptions

def check_valid_schema(schema, data):
  try:
    validate(data, schema)
    return True
  except exceptions.ValidationError as error:
    print(f"\n\n\033[91mValidation Error: {error.message}")
    return False
