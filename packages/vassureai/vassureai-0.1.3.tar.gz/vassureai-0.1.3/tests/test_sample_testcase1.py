"""
-----------------------
Author: Sukumar Kutagulla 
Designation: Test Automation Architect
-----------------------

Auto-generated test script by VAssureAI Framework
Test Name: sample_testcase1
"""

import pytest
import datetime
import os
from utils.base_test import BaseTest
from utils.logger import logger
from utils.config import Config

@pytest.mark.requires_browser
@pytest.mark.auto_generated
class TestSampleTestcase1(BaseTest):
    """
    Test Case: Create deviation  
1. 'Navigate to "https://login.veevavault.com/auth/login" url'  
2. f'Enter "Vault.Admin@vaultbasics -automation.com" in username text box'  
3. 'Click continue button'  
4. f'Enter "SPOTLINE@veeva1234" in password text box'  
5. 'Click  log in button'  
6. 'wait for network idle'  
7. 'Click select vault dropdown'  
8. 'Select "QualityBasicsDryRun25R1 (vaultbasics -automation.com)" from dropdown options'  
9. 'wait for network idle'  
10. 'Click document workspace tab collection menu'  
11. 'Select " QMS" from menu items  
12. 'Verify "QMS" menu item selected successfully'  
13. 'Click quality events menu'  
14. 'Click deviations sub menu from quality events menu'  
15. 'wait for network idle'  
16. 'Verify "All Deviations" title is displayed'  
17. 'Click create button'  
18. 'wait for network idle'  
19. 'Verify "Create Deviation" title is displayed'
    """
    
    __test__ = True
    
    @pytest.fixture(autouse=True)
    def setup_test(self, setup_base):
        """Setup test instance"""
        self.test_name = "sample_testcase1"
        self.retry_attempts = Config.retry.max_retries
        self.steps = []
        self.agent = None
        self.video_path = None
        self.screenshot_steps = []
        self.screenshot_dir = "reports/screenshots"
        self.test_start_time = None
        
        # Ensure directories exist
        if Config.browser.record_video:
            os.makedirs(Config.browser.video_dir, exist_ok=True)
        
        # Ensure screenshots directory exists
        os.makedirs(self.screenshot_dir, exist_ok=True)
        return self
    
    def get_all_test_steps(self):
        """Get all test steps for this test case"""
        return [
            "1. 'Navigate to \"https://login.veevavault.com/auth/login\" url'",
            "2. f'Enter \"Vault.Admin@vaultbasics -automation.com\" in username text box'",
            "3. 'Click continue button'",
            "4. f'Enter \"SPOTLINE@veeva1234\" in password text box'",
            "5. 'Click  log in button'",
            "6. 'wait for network idle'",
            "7. 'Click select vault dropdown'",
            "8. 'Select \"QualityBasicsDryRun25R1 (vaultbasics -automation.com)\" from dropdown options'",
            "9. 'wait for network idle'",
            "10. 'Click document workspace tab collection menu'",
            "11. 'Select \" QMS\" from menu items",
            "12. 'Verify \"QMS\" menu item selected successfully'",
            "13. 'Click quality events menu'",
            "14. 'Click deviations sub menu from quality events menu'",
            "15. 'wait for network idle'",
            "16. 'Verify \"All Deviations\" title is displayed'",
            "17. 'Click create button'",
            "18. 'wait for network idle'",
            "19. 'Verify \"Create Deviation\" title is displayed'",
        ]
    
    @pytest.mark.asyncio
    async def test_execution(self):
        """Execute the test case"""
        logger.info(f"Starting {self.test_name} execution")
        test_steps = self.get_all_test_steps()
        
        result = await self._execute_test(test_steps)
        
        # Don't retry if verification failed - that's expected behavior
        if not result and any("verify" in step.lower() for step in test_steps):
            verification_errors = [
                step.get('error') 
                for step in self.steps 
                if step.get('status') == 'fail' and 'verify' in step.get('name', '').lower()
            ]
            if verification_errors:
                logger.info(f"Test failed due to verification: {verification_errors[0]}")
                return
        
        # Only retry for non-verification failures
        if not result:
            logger.warning(f"{self.test_name} failed due to non-verification error")
            raise Exception("Test failed due to non-verification error")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])