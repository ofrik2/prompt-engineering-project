"""
Unit tests for Azure OpenAI Helper validation and configuration.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from azure_openai_helper import validate_configuration, llm_query
from azure_openai_helper.llm_client import ConfigurationError


def test_configuration_validation():
    """
    Test that configuration loads successfully from .env file.
    """
    print("=" * 60)
    print("Testing Configuration Validation")
    print("=" * 60)
    
    try:
        result = validate_configuration()
        print("✓ Configuration validation passed!")
        print(f"  Result: {result}")
        
        # Check that environment variables are loaded
        required_vars = [
            'AZURE_OPENAI_ENDPOINT',
            'AZURE_OPENAI_API_KEY',
            'AZURE_OPENAI_DEPLOYMENT_NAME',
            'AZURE_OPENAI_API_VERSION'
        ]
        
        print("\n✓ Environment variables loaded:")
        for var in required_vars:
            value = os.getenv(var)
            if value:
                # Mask sensitive values
                if 'KEY' in var:
                    display_value = value[:10] + "..." + value[-10:] if len(value) > 20 else "***"
                else:
                    display_value = value
                print(f"  - {var}: {display_value}")
            else:
                print(f"  - {var}: NOT FOUND")
                
        return True
        
    except ConfigurationError as e:
        print(f"✗ Configuration validation failed!")
        print(f"  Error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during validation!")
        print(f"  Error: {e}")
        return False


def test_simple_query():
    """
    Test a simple query to verify the module works end-to-end.
    """
    print("\n" + "=" * 60)
    print("Testing Simple LLM Query")
    print("=" * 60)
    
    test_prompt = "Say 'Hello, Context Window Labs!' and nothing else."
    
    try:
        print(f"\nSending prompt: '{test_prompt}'")
        print("\nWaiting for response...")
        
        response = llm_query(
            prompt=test_prompt,
            temperature=0.0,
            max_tokens=50
        )
        
        print("\n✓ Query successful!")
        print(f"\nResponse:\n{response}")
        
        return True
        
    except ConfigurationError as e:
        print(f"\n✗ Configuration error!")
        print(f"  Error: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Query failed!")
        print(f"  Error: {e}")
        return False


def test_parameter_validation():
    """
    Test that parameter validation works correctly.
    """
    print("\n" + "=" * 60)
    print("Testing Parameter Validation")
    print("=" * 60)
    
    test_cases = [
        {
            'name': 'Empty prompt',
            'prompt': '',
            'should_fail': True,
            'error_type': ValueError
        },
        {
            'name': 'Invalid temperature (too high)',
            'prompt': 'test',
            'temperature': 3.0,
            'should_fail': True,
            'error_type': ValueError
        },
        {
            'name': 'Invalid temperature (negative)',
            'prompt': 'test',
            'temperature': -0.5,
            'should_fail': True,
            'error_type': ValueError
        },
        {
            'name': 'Invalid max_tokens (negative)',
            'prompt': 'test',
            'max_tokens': -100,
            'should_fail': True,
            'error_type': ValueError
        },
        {
            'name': 'Invalid max_tokens (zero)',
            'prompt': 'test',
            'max_tokens': 0,
            'should_fail': True,
            'error_type': ValueError
        }
    ]
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        print(f"\nTest: {test_case['name']}")
        
        try:
            kwargs = {'prompt': test_case['prompt']}
            if 'temperature' in test_case:
                kwargs['temperature'] = test_case['temperature']
            if 'max_tokens' in test_case:
                kwargs['max_tokens'] = test_case['max_tokens']
            
            # This should raise an error for invalid inputs
            # We set max_tokens=1 to avoid making actual API calls
            if not test_case['should_fail']:
                kwargs['max_tokens'] = 1
                
            result = llm_query(**kwargs)
            
            if test_case['should_fail']:
                print(f"  ✗ Expected {test_case['error_type'].__name__} but no error was raised")
                failed += 1
            else:
                print(f"  ✓ Passed as expected")
                passed += 1
                
        except Exception as e:
            if test_case['should_fail'] and isinstance(e, test_case['error_type']):
                print(f"  ✓ Correctly raised {type(e).__name__}: {e}")
                passed += 1
            else:
                print(f"  ✗ Unexpected error: {type(e).__name__}: {e}")
                failed += 1
    
    print(f"\n{'=' * 60}")
    print(f"Parameter validation results: {passed} passed, {failed} failed")
    
    return failed == 0


def run_all_tests():
    """
    Run all validation tests.
    """
    print("\n" + "=" * 60)
    print("AZURE OPENAI HELPER - VALIDATION TESTS")
    print("=" * 60)
    
    results = {
        'Configuration Validation': test_configuration_validation(),
        'Parameter Validation': test_parameter_validation(),
        'Simple Query': test_simple_query()
    }
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED! ✓")
    else:
        print("SOME TESTS FAILED! ✗")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
