import boto3

aws_region_name = 'eu-west-3'

def get_region_name():
    return aws_region_name

### SSM Parameter Store ###

def get_parameter(system, param_name = None):
    try:
        ssm = boto3.client('ssm', region_name=aws_region_name)

        if param_name is not None:
            if 'password' in param_name or 'secret' in param_name:
                parameter = ssm.get_parameter(Name=f'/{system}/{param_name}', WithDecryption=True)
                param_value = parameter['Parameter']['Value']
            else:
                parameter = ssm.get_parameter(Name=f'/{system}/{param_name}')
                param_value = parameter['Parameter']['Value']
        else:
            parameter = ssm.get_parameter(Name=f'/{system}')
            param_value = parameter['Parameter']['Value']

        return param_value
    except Exception as e:
        print(f"An error occurred while trying to retrieve parameter {param_name} : {e}")

def get_parameters(path, with_decryption = False):
    try:
        ssm = boto3.client('ssm', region_name=aws_region_name)

        parameters = ssm.get_parameters_by_path(
            Path=path,
            Recursive=True,
            WithDecryption=with_decryption
        )

        return parameters['Parameters']
    except Exception as e:
        print(f"An error occurred while trying to retrieve parameters by path {path} : {e}")

def extract_parameter(parameter_list, parameter_name):
    return next((parameter['Value'] for parameter in parameter_list if parameter_name in parameter['Name']), None)