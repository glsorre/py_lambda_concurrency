import json
import pickle

import boto3

from botocore.config import Config

RUNS = [
    # {
    #     'executor': 'processpool|threadpool|sequential',
    #     'pool_size': 'cpu_count|integer',
    #     'tot_number': 4,
    #     'function_name': 'io_bounded_func|cpu_bounded_func|cpu_bounded_func_quick',
    #     'function_arg': "'https://docs.python.org/3/'"
    # }
    {   
        'lambdas':[
            'py_lambda_concurrency_stress_768',
            'py_lambda_concurrency_stress_1280',
            'py_lambda_concurrency_stress_1792',
            'py_lambda_concurrency_stress_2304',
            'py_lambda_concurrency_stress_2816'
        ],
        'executor': 'processpool',
        'pool_size': 'cpu_count',
        'tot_number': 200,
        'function_name': 'cpu_bounded_func_quick',
        'function_arg': "[randint(10, 10000) for x in range(10000)]"
    },
    {   
        'lambdas':[
            'py_lambda_concurrency_stress_768',
            'py_lambda_concurrency_stress_1280',
            'py_lambda_concurrency_stress_1792',
            'py_lambda_concurrency_stress_2304',
            'py_lambda_concurrency_stress_2816'
        ],
        'executor': 'threadpool',
        'pool_size': 'cpu_count',
        'tot_number': 200,
        'function_name': 'cpu_bounded_func_quick',
        'function_arg': "[randint(10, 10000) for x in range(10000)]"
    },
    {   
        'lambdas':[
            'py_lambda_concurrency_stress_768',
            'py_lambda_concurrency_stress_1280',
            'py_lambda_concurrency_stress_1792',
            'py_lambda_concurrency_stress_2304',
            'py_lambda_concurrency_stress_2816'
        ],
        'executor': 'sequential',
        'pool_size': 'cpu_count',
        'tot_number': 200,
        'function_name': 'cpu_bounded_func_quick',
        'function_arg': "[randint(10, 10000) for x in range(10000)]"
    }
    # {   
    #     'lambdas':[
    #         'py_lambda_concurrency_stress_2816'
    #     ],
    #     'executor': 'processpool',
    #     'pool_size': 'cpu_count',
    #     'tot_number': 100,
    #     'function_name': 'cpu_bounded_func',
    #     'function_arg': "[randint(10, 10000) for x in range(10000)]"
    # },
    # {   
    #     'lambdas':[
    #         'py_lambda_concurrency_stress_2816'
    #     ],
    #     'executor': 'threadpool',
    #     'pool_size': 'cpu_count',
    #     'tot_number': 100,
    #     'function_name': 'cpu_bounded_func',
    #     'function_arg': "[randint(10, 10000) for x in range(10000)]"
    # },
    # {   
    #     'lambdas':[
    #         'py_lambda_concurrency_stress_2816'
    #     ],
    #     'executor': 'sequential',
    #     'pool_size': 'cpu_count',
    #     'tot_number': 100,
    #     'function_name': 'cpu_bounded_func',
    #     'function_arg': "[randint(10, 10000) for x in range(10000)]"
    # }
    # {   
    #     'lambdas':[
    #         'py_lambda_concurrency_stress_768',
    #         'py_lambda_concurrency_stress_1280',
    #         'py_lambda_concurrency_stress_1792',
    #         'py_lambda_concurrency_stress_2304',
    #         'py_lambda_concurrency_stress_2816'
    #     ],
    #     'executor': 'processpool',
    #     'pool_size': 'cpu_count',
    #     'tot_number': 200,
    #     'function_name': 'io_bounded_func',
    #     'function_arg': "'https://docs.python.org/3/'"
    # },
    # {   
    #     'lambdas':[
    #         'py_lambda_concurrency_stress_768',
    #         'py_lambda_concurrency_stress_1280',
    #         'py_lambda_concurrency_stress_1792',
    #         'py_lambda_concurrency_stress_2304',
    #         'py_lambda_concurrency_stress_2816'
    #     ],
    #     'executor': 'threadpool',
    #     'pool_size': 'cpu_count',
    #     'tot_number': 200,
    #     'function_name': 'io_bounded_func',
    #     'function_arg': "'https://docs.python.org/3/'"
    # },
    # {   
    #     'lambdas':[
    #         'py_lambda_concurrency_stress_768',
    #         'py_lambda_concurrency_stress_1280',
    #         'py_lambda_concurrency_stress_1792',
    #         'py_lambda_concurrency_stress_2304',
    #         'py_lambda_concurrency_stress_2816'
    #     ],
    #     'executor': 'sequential',
    #     'pool_size': 'cpu_count',
    #     'tot_number': 200,
    #     'function_name': 'io_bounded_func',
    #     'function_arg': "'https://docs.python.org/3/'"
    # }
    # {   
    #     'lambdas':[
    #         'py_lambda_concurrency_stress_1792'
    #     ],
    #     'executor': 'processpool',
    #     'pool_size': 'cpu_count',
    #     'tot_number': 2000,
    #     'function_name': 'io_bounded_func',
    #     'function_arg': "'https://docs.python.org/3/'"
    # },
    # {   
    #     'lambdas':[
    #         'py_lambda_concurrency_stress_1792'
    #     ],
    #     'executor': 'threadpool',
    #     'pool_size': 'cpu_count',
    #     'tot_number': 2000,
    #     'function_name': 'io_bounded_func',
    #     'function_arg': "'https://docs.python.org/3/'"
    # },
    # {   
    #     'lambdas':[
    #         'py_lambda_concurrency_stress_1792'
    #     ],
    #     'executor': 'sequential',
    #     'pool_size': 'cpu_count',
    #     'tot_number': 2000,
    #     'function_name': 'io_bounded_func',
    #     'function_arg': "'https://docs.python.org/3/'"
    # }
]

if __name__ == "__main__":
    lambda_client = boto3.client(
        service_name='lambda',
        config=Config(read_timeout=900, retries={'max_attempts': 0})
        )

    results = []

    for r in RUNS:
        for l in r['lambdas']:
            print(r, r['executor'], r['function_name'])
            response = lambda_client.invoke(
                FunctionName=l,
                InvocationType='RequestResponse',
                Payload=json.dumps({
                    'executor': r['executor'],
                    'pool_size': r['pool_size'],
                    'tot_number': r['tot_number'],
                    'function_name': r['function_name'],
                    'function_arg': r['function_arg']
                })
            )
            result = eval(response['Payload'].read().decode())
            result['lambda'] = l
            results.append(result)

    print([i['final_time'] for i in results])

    with open('stress_data.pickle', 'wb') as f:
        pickle.dump(results, f)