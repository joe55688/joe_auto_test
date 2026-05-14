"""Module for screenshot comparison and matching"""

import logging
import cv2
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
from PIL import ImageGrab

logger = logging.getLogger(__name__)


class ScreenshotMatcher:
    """Compares screenshots and finds matches"""

    def __init__(self, threshold: float = 0.85):
        """Initialize the screenshot matcher
        
        Args:
            threshold: Similarity threshold (0-1)
        """
        self.threshold = threshold

    def capture_screenshot(self, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """Capture a screenshot
        
        Args:
            region: Optional (left, top, right, bottom) tuple for partial screenshot
            
        Returns:
            Screenshot as numpy array
        """
        try:
            if region:
                screenshot = ImageGrab.grab(bbox=region)
            else:
                screenshot = ImageGrab.grab()
            
            # Convert PIL Image to numpy array
            screenshot_array = np.array(screenshot)
            # Convert RGB to BGR for OpenCV
            screenshot_array = cv2.cvtColor(screenshot_array, cv2.COLOR_RGB2BGR)
            
            logger.info("Screenshot captured")
            return screenshot_array
        except Exception as e:
            logger.error(f"Error capturing screenshot: {e}")
            return None

    def save_screenshot(self, image: np.ndarray, filepath: str) -> bool:
        """Save screenshot to file
        
        Args:
            image: Screenshot as numpy array
            filepath: Path to save the screenshot
            
        Returns:
            True if successful
        """
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(filepath, image)
            logger.info(f"Screenshot saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving screenshot: {e}")
            return False

    def load_screenshot(self, filepath: str) -> np.ndarray:
        """Load screenshot from file
        
        Args:
            filepath: Path to the screenshot
            
        Returns:
            Screenshot as numpy array
        """
        try:
            image = cv2.imread(filepath)
            if image is None:
                raise ValueError(f"Could not load image from {filepath}")
            logger.info(f"Screenshot loaded from {filepath}")
            return image
        except Exception as e:
            logger.error(f"Error loading screenshot: {e}")
            return None

    def compare(self, image1: np.ndarray, image2: np.ndarray) -> float:
        """Compare two images using multiple methods
        
        Args:
            image1: First image as numpy array
            image2: Second image as numpy array
            
        Returns:
            Similarity score (0-1)
        """
        if image1 is None or image2 is None:
            logger.error("Invalid image provided for comparison")
            return 0.0

        try:
            # Method 1: Histogram comparison
            hist_score = self._compare_histograms(image1, image2)
            
            # Method 2: Template matching (if same size)
            if image1.shape == image2.shape:
                mse_score = self._compare_mse(image1, image2)
            else:
                mse_score = 0.0
            
            # Method 3: Feature matching
            feature_score = self._compare_features(image1, image2)
            
            # Average the scores
            final_score = (hist_score * 0.3 + mse_score * 0.4 + feature_score * 0.3)
            
            logger.info(f"Comparison result: {final_score:.2%}")
            return final_score
            
        except Exception as e:
            logger.error(f"Error comparing images: {e}")
            return 0.0

    def _compare_histograms(self, image1: np.ndarray, image2: np.ndarray) -> float:
        """Compare images using histogram
        
        Args:
            image1: First image
            image2: Second image
            
        Returns:
            Similarity score (0-1)
        """
        try:
            # Convert to HSV for better color comparison
            hsv1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
            hsv2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
            
            # Calculate histograms
            hist1 = cv2.calcHist([hsv1], [0, 1], None, [180, 256], [0, 180, 0, 256])
            hist2 = cv2.calcHist([hsv2], [0, 1], None, [180, 256], [0, 180, 0, 256])
            
            # Normalize histograms
            cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
            cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
            
            # Compare using Bhattacharyya distance
            score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
            return 1.0 - score  # Convert distance to similarity
            
        except Exception as e:
            logger.debug(f"Error in histogram comparison: {e}")
            return 0.0

    def _compare_mse(self, image1: np.ndarray, image2: np.ndarray) -> float:
        """Compare images using Mean Squared Error
        
        Args:
            image1: First image
            image2: Second image
            
        Returns:
            Similarity score (0-1)
        """
        try:
            # Calculate MSE
            mse = np.mean((image1.astype(float) - image2.astype(float)) ** 2)
            
            # Normalize MSE to 0-1 range
            max_possible_mse = 255 ** 2
            score = 1.0 - (mse / max_possible_mse)
            
            return max(0.0, min(1.0, score))
            
        except Exception as e:
            logger.debug(f"Error in MSE comparison: {e}")
            return 0.0

    def _compare_features(self, image1: np.ndarray, image2: np.ndarray) -> float:
        """Compare images using ORB feature matching
        
        Args:
            image1: First image
            image2: Second image
            
        Returns:
            Similarity score (0-1)
        """
        try:
            # Initialize ORB detector
            orb = cv2.ORB_create(nfeatures=500)
            
            # Find keypoints and descriptors
            kp1, des1 = orb.detectAndCompute(image1, None)
            kp2, des2 = orb.detectAndCompute(image2, None)
            
            if des1 is None or des2 is None:
                return 0.0
            
            # Match descriptors
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)
            
            # Sort matches by distance
            matches = sorted(matches, key=lambda x: x.distance)
            
            # Calculate match score
            if len(matches) == 0:
                return 0.0
            
            # Average distance of matches
            avg_distance = np.mean([m.distance for m in matches])
            
            # Convert distance to similarity (lower distance = higher similarity)
            score = 1.0 - (avg_distance / 100.0)
            
            return max(0.0, min(1.0, score))
            
        except Exception as e:
            logger.debug(f"Error in feature comparison: {e}")
            return 0.0

    def find_template(self, image: np.ndarray, template: np.ndarray) -> Optional[Tuple[int, int, float]]:
        """Find template in image
        
        Args:
            image: Image to search in
            template: Template to search for
            
        Returns:
            Tuple of (x, y, match_score) or None if not found
        """
        try:
            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= self.threshold:
                return (max_loc[0], max_loc[1], max_val)
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error finding template: {e}")
            return None
