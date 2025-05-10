import os
import time
from seleniumbase import SB
from .captcha_replicator import CaptchaReplicator
from .audio_challenge_solver import AudioChallengeSolver


# it receives captcha params, outputs solve token 
# the audio challenge solver receives a browser instance with the emulated captcha page loaded
class CaptchaSolver:
    """
    Main entry point for solving reCAPTCHAs.
    
    This class handles the core captcha solving process. It focuses only on solving
    and does not handle extraction or application of tokens, maintaining clear separation
    of concerns and modularity.
    
    Usage example:
        # With params already extracted
        solver = CaptchaSolver(wit_api_key="YOUR_API_KEY")
        token, success = solver.solve(params)
        
        # Or with a full workflow using helper classes:
        from captcha_solver import CaptchaExtractor, TokenSubmitter
        
        extractor = CaptchaExtractor()
        params = extractor.extract_captcha_params(browser)
        
        solver = CaptchaSolver(wit_api_key="YOUR_API_KEY")
        token, success = solver.solve(params)
        
        submitter = TokenSubmitter()
        submitter.apply_token(browser, token, params)
    """
    
    def __init__(self, wit_api_key=None, download_dir="tmp"):
        """
        Initialize the CaptchaSolver with required dependencies.
        
        Args:
            wit_api_key (str, optional): API key for Wit.ai speech recognition
            download_dir (str, optional): Directory for temporary files
        """
        self.wit_api_key = wit_api_key
        self.download_dir = download_dir
        
        # Create internal components
        self.replicator = CaptchaReplicator(download_dir=download_dir)
        self.challenge_solver = AudioChallengeSolver(wit_api_key=wit_api_key, download_dir=download_dir)
        
        # Ensure the download directory exists
        os.makedirs(self.download_dir, exist_ok=True)
    
    def solve(self, params):
        """
        Solve the captcha based on provided parameters.
        
        Args:
            params (dict): Dictionary containing captcha parameters:
                - website_key (str): reCAPTCHA site key
                - website_url (str): URL where captcha appears
                - is_invisible (bool, optional): Whether it's invisible
                - data_s_value (str, optional): data-s parameter if present
                - is_enterprise (bool, optional): If it's enterprise reCAPTCHA
            
        Returns:
            tuple: (token, success_status)
                - token (str): The solved reCAPTCHA token if successful, None otherwise
                - success_status (bool): Whether the solving was successful
        """
        print("\n=== Solving reCAPTCHA with Provided Parameters ===")
        print(f"Site key: {params.get('website_key')}")
        print(f"Website URL: {params.get('website_url')}")
        print(f"Is invisible: {params.get('is_invisible', False)}")
        print(f"Is enterprise: {params.get('is_enterprise', False)}")
        
        # Validate required parameters
        if not params.get("website_key") or not params.get("website_url"):
            print("ERROR: Missing required parameters (website_key and website_url)")
            return None, False
        
        try:
            # Create a SeleniumBase browser instance
            print("\n--- Step 1: Creating browser instance ---")
            
            # PROPERLY USE THE CONTEXT MANAGER WITH 'with' STATEMENT
            with SB(uc=False, headless=False, test=True, locale="en") as browser:
                print(f"Browser instance created: {type(browser)}")
                
                # Set up the captcha in the browser
                print("\n--- Step 2: Setting up reCAPTCHA ---")
                html_path, initial_token = self.replicator.replicate_captcha(
                    website_key=params["website_key"],
                    website_url=params["website_url"],
                    browser=browser,
                    is_invisible=params.get("is_invisible", False),
                    data_s_value=params.get("data_s_value"),
                    is_enterprise=params.get("is_enterprise", False),
                    observation_time=5,  # Just enough time to load the CAPTCHA

                    bypass_domain_check=True,  # Enable hosts file bypass
                    use_ssl=True  # Use SSL with self-signed certificate

                )
                
                # If we couldn't set up the captcha
                if not html_path:
                    print("ERROR: Failed to set up CAPTCHA. Aborting.")
                    return None, False
                
                # If we already have an initial token from setup, return it
                if initial_token and len(initial_token) > 20:  # Basic validation
                    print(f"Initial token found during setup: {initial_token[:20]}...")
                    return initial_token, True
                    
                # Solve the challenge with the browser instance
                print("\n--- Step 3: Solving reCAPTCHA Challenge ---")
                token, success = self.challenge_solver.solve(browser)
                
                # If solving failed, check if token was captured by monitor thread
                if not success or not token:
                    print("Direct solving unsuccessful, checking monitor thread...")
                    token = self.replicator.get_last_token()
                    if token:
                        success = True
                        print(f"Token found from monitor thread: {token[:20]}...")
                    else:
                        print("No token found from monitor thread.")
                
                if success and token:
                    print(f"\n✅ reCAPTCHA solved successfully!")
                    print(f"Token (first 20 chars): {token[:20]}...")
                else:
                    print("\n❌ Failed to solve reCAPTCHA")
                    
                return token, success
            
        except Exception as e:
            print(f"ERROR during solving process: {e}")
            import traceback
            traceback.print_exc()
            return None, False
            
        finally:
            # Clean up resources - no need to close browser as it's handled by the context manager
            print("\n--- Cleaning Up Resources ---")
            try:
                print("Stopping HTTP server...")
                self.replicator.stop_http_server()
            except Exception as e:
                print(f"Error stopping server: {e}")

if __name__ == "__main__":
    # Test the solver
    print("\n=== Testing CaptchaSolver ===")
    captcha_params = {
        "website_key": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
        "website_url": "https://www.google.com/recaptcha/api2/demo",
        "is_invisible": False,
        "is_enterprise": False,
        "data_s_value": None  # This parameter is usually None for standard reCAPTCHA
    }

    # Initialize solver
    solver = CaptchaSolver(wit_api_key="YOUR_API_KEY")

    # Run the workflow
    token, success = solver.solve(captcha_params)
    print(f"--> Solved: {success}")
    if success and token:
        print(f"--> Token: {token[:20]}...")
    else:
        print("--> No token received")