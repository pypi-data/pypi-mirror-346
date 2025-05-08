from typing import Optional, Tuple, Union, List

import cv2
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image
import mss
import mss.windows

def capture_screen(region: Optional[Tuple[int, int, int, int]] = None) -> Image.Image:
    """Capture a screenshot of the entire screen or a specific region.
    
    Args:
        region: Optional tuple of (left, top, right, bottom) coordinates.
               If None, captures the entire screen.
               
    Returns:
        PIL Image object containing the screenshot.
        
    Raises:
        mss.exception.ScreenShotError: If screen capture fails.
    """
    with mss.mss() as sct:
        if region is None:
            monitor = sct.monitors[0]  # Primary monitor
            region = (monitor['left'], monitor['top'], 
                     monitor['left'] + monitor['width'], 
                     monitor['top'] + monitor['height'])
        
        # Convert to MSS format
        capture_area = {
            'left': region[0],
            'top': region[1],
            'width': region[2] - region[0],
            'height': region[3] - region[1]
        }
        
        # Capture and convert to PIL Image
        sct_img = sct.grab(capture_area)
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

def capture_window(hwnd: int) -> Optional[Image.Image]:
    """Capture a screenshot of a specific window.
    
    Args:
        hwnd: Window handle.
        
    Returns:
        PIL Image object containing the window screenshot,
        or None if the window handle is invalid.
        
    Raises:
        mss.exception.ScreenShotError: If window capture fails.
    """
    try:
        # Get window dimensions using MSS Windows-specific implementation
        with mss.windows.MSS() as sct:
            rect = sct.get_window_rect(hwnd)
            capture_area = {
                'left': rect.left,
                'top': rect.top,
                'width': rect.right - rect.left,
                'height': rect.bottom - rect.top
            }
            
            # Capture and convert to PIL Image
            sct_img = sct.grab(capture_area)
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
    except Exception:
        return None

def convert_to_grayscale(image: Union[np.ndarray, Image.Image]) -> np.ndarray:
    """Convert image to grayscale.
    
    Args:
        image: Input image (OpenCV or PIL Image).
        
    Returns:
        Grayscale image as numpy array.
    """
    if isinstance(image, Image.Image):
        image = np.array(image)
    
    if len(image.shape) == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def color_quantization(image: np.ndarray, levels: int) -> np.ndarray:
    """Reduce number of colors in image using k-means clustering.
    
    Args:
        image: Input image as numpy array.
        levels: Number of color levels to quantize to.
        
    Returns:
        Color quantized image.
    """
    h, w = image.shape[:2]
    image = np.float32(image).reshape(-1, 3)
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(image, levels, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape((h, w, 3))

def apply_threshold(image: np.ndarray, method: str = 'global', block_size: int = 11, c: int = 2) -> np.ndarray:
    """Apply thresholding to grayscale image.
    
    Args:
        image: Grayscale input image.
        method: Thresholding method ('global' or 'adaptive').
        block_size: Block size for adaptive threshold (must be odd).
        c: Constant subtracted from mean for adaptive threshold.
        
    Returns:
        Binary image.
    """
    if len(image.shape) > 2:
        image = convert_to_grayscale(image)
        
    if method == 'global':
        _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        binary = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, block_size, c
        )
    return binary

def morphological_cleanup(image: np.ndarray, operation: str = 'clean', kernel_size: int = 3) -> np.ndarray:
    """Apply morphological operations for cleanup.
    
    Args:
        image: Binary input image.
        operation: Type of cleanup ('clean', 'dilate', 'erode').
        kernel_size: Size of the kernel for morphological operation.
        
    Returns:
        Cleaned binary image.
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    
    if operation == 'clean':
        # Remove small noise and fill small holes
        image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    elif operation == 'dilate':
        image = cv2.dilate(image, kernel, iterations=1)
    elif operation == 'erode':
        image = cv2.erode(image, kernel, iterations=1)
        
    return image

def apply_smoothing(image: np.ndarray, method: str = 'gaussian', kernel_size: int = 3) -> np.ndarray:
    """Apply smoothing filter to image.
    
    Args:
        image: Input image.
        method: Smoothing method ('gaussian', 'median', or 'bilateral').
        kernel_size: Size of the kernel (must be odd).
        
    Returns:
        Smoothed image.
    """
    if method == 'gaussian':
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    elif method == 'median':
        return cv2.medianBlur(image, kernel_size)
    elif method == 'bilateral':
        return cv2.bilateralFilter(image, kernel_size, 75, 75)
    return image

def down_sample(image: np.ndarray, scale_factor: float) -> np.ndarray:
    """Reduce image size by given scale factor.
    
    Args:
        image: Input image.
        scale_factor: Factor to scale image by (0 < scale_factor <= 1).
        
    Returns:
        Downsampled image.
    """
    if not 0 < scale_factor <= 1:
        raise ValueError("Scale factor must be between 0 and 1")
        
    width = int(image.shape[1] * scale_factor)
    height = int(image.shape[0] * scale_factor)
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

from paddleocr import PaddleOCR
ocr = PaddleOCR(lang = 'ch', show_log = False, use_angle_cls = True)

def extract_text(image: Union[np.ndarray, Image.Image]):
    """Extract text from image using PaddleOCR.
    
    Args:
        image: Input image (OpenCV or PIL Image).
        lang: Language(s) for OCR (default is Chinese). Can be string or list of strings.
            Examples: 'ch', 'en', ['ch', 'en']
        
    Returns:
        Location, extracted text, and confidence score for each detected text region.
    """
    image = preprocess_for_ocr(image)
    
    
    if isinstance(image, Image.Image):
        image = np.array(image)
    
    result = ocr.ocr(image, cls=True)
    
    # Extract and join all detected text
    return result

def preprocess_for_ocr(image: Union[np.ndarray, Image.Image], 
                      scale_factor: float = 1.0,
                      threshold_method: str = 'adaptive') -> np.ndarray:
    """Apply comprehensive preprocessing for OCR.
    
    Args:
        image: Input image.
        scale_factor: Factor to scale image by (0 < scale_factor <= 1).
        threshold_method: Thresholding method ('global' or 'adaptive').
        
    Returns:
        Preprocessed image ready for OCR.
    """
    if isinstance(image, Image.Image):
        image = np.array(image)
    
    # Downscale if requested
    if scale_factor < 1.0:
        image = down_sample(image, scale_factor)
    
    # Convert to grayscale
    rst = color_quantization(image, 4)
    rst = convert_to_grayscale(rst)
    
    return rst

def preprocess_for_template(image: np.ndarray) -> np.ndarray:
    """Preprocess image for template matching.
    
    Args:
        image: Input image as numpy array.
        
    Returns:
        Preprocessed image optimized for template matching.
    """
    # Convert to grayscale
    gray = convert_to_grayscale(image)
    
    # Apply Gaussian blur to reduce noise
    blurred = apply_smoothing(gray, method='gaussian', kernel_size=5)
    
    # Apply adaptive thresholding
    binary = apply_threshold(blurred, method='adaptive', block_size=11, c=2)
    
    return binary

def find_pattern(source: np.ndarray, pattern: List[Tuple[int, int, Tuple[int, int, int]]], threshold: float = 0.8) -> List[Tuple[int, int, float]]:
    """Find color pattern matches in source image.
    
    Args:
        source: Source image to search in (RGB format).
        pattern: List of relative points as (dx, dy, (r, g, b)).
        threshold: Matching threshold (0-1).
        
    Returns:
        List of (x, y, score) tuples where pattern matches were found.
    """
    if len(source.shape) != 3 or source.shape[2] != 3:
        raise ValueError("Source image must be in RGB format")
    
    height, width = source.shape[:2]
    matches = []
    
    # Precompute pattern bounds to avoid out-of-bounds checks
    min_dx = min(p[0] for p in pattern)
    max_dx = max(p[0] for p in pattern)
    min_dy = min(p[1] for p in pattern)
    max_dy = max(p[1] for p in pattern)
    
    # Calculate valid search area
    start_x = max(0, -min_dx)
    end_x = min(width, width - max_dx)
    start_y = max(0, -min_dy)
    end_y = min(height, height - max_dy)
    
    # Convert pattern colors to numpy array for vectorized operations
    pattern_colors = np.array([p[2] for p in pattern], dtype=np.float32)
    
    score_for_each_point = []
    # Calculate scores for each point
    for dx, dy, color in pattern:
        score   = np.full((height, width), 0, dtype=np.float32)

        # Calculate valid coordinates for this pattern point
        x_start = max(0, -dx)
        x_end   = min(width, width - dx)
        y_start = max(0, -dy)
        y_end   = min(height, height - dy)
        
        # Extract source colors for valid coordinates
        source_colors = source[y_start:y_end, x_start:x_end]
        
        # Calculate color differences and scores
        diff = np.linalg.norm(source_colors - color, axis=2)
        point_scores = 1 - (diff / (255 * np.sqrt(3)))
        
        # Accumulate scores
        score[y_start:y_end, x_start:x_end] = point_scores
        score_for_each_point.append(score)

    def _shift_array(arr, shift_x, shift_y):
        rst = np.full(arr.shape, np.nan, dtype=np.float32)
        if shift_x > 0 and shift_y > 0:
            rst[shift_y:, shift_x:] = arr[:-shift_y, :-shift_x]
        elif shift_x < 0 and shift_y > 0:
            rst[shift_y:, :shift_x] = arr[:-shift_y, -shift_x:]
        elif shift_x > 0 and shift_y < 0:
            rst[:shift_y, shift_x:] = arr[-shift_y:, :-shift_x]
        elif shift_x < 0 and shift_y < 0:
            rst[:shift_y, :shift_x] = arr[-shift_y:, -shift_x:]
        elif shift_x == 0 and shift_y > 0:
            rst[shift_y:, :] = arr[:-shift_y, :]
        elif shift_x == 0 and shift_y < 0:
            rst[:shift_y, :] = arr[-shift_y:, :]
        elif shift_x > 0 and shift_y == 0:
            rst[:, shift_x:] = arr[:, :-shift_x]
        elif shift_x < 0 and shift_y == 0:
            rst[:, :shift_x] = arr[:, -shift_x:]
        else:
            rst[:] = arr[:]
        return rst
    
    # Create score array matching source image dimensions
    scores = np.zeros((height, width), dtype=np.float32)
    for idx, (dx, dy, color) in enumerate(pattern):
        scores += _shift_array(score_for_each_point[idx], -dx, -dy)

    # Average scores across pattern points
    scores = scores / len(pattern)
    
    # Find matches above threshold
    match_coords = np.argwhere(scores >= threshold)
    
    # If no matches, return empty list
    if len(match_coords) == 0:
        return []
        
    # Find the best match (highest score)
    best_score = np.nanmax(scores)
    best_matches = np.argwhere(scores == best_score)
    
    # Convert to list of (x, y, score) tuples
    for y, x in best_matches:
        matches.append((x, y, scores[y, x]))
    
    return matches

def find_image(source: Union[np.ndarray, Image.Image], template: Union[np.ndarray, Image.Image], threshold: float = 0.8) -> List[Tuple[int, int]]:
    """Find template matches in source image.
    
    Args:
        source: Source image to search in.
        template: Template image to search for.
        threshold: Matching threshold (0-1).
        
    Returns:
        List of (x,y) coordinates where matches were found.
    """
    # Preprocess both images
    source_preprocessed = preprocess_for_template(source)
    template_preprocessed = preprocess_for_template(template)
    
    # Perform template matching
    result = cv2.matchTemplate(source_preprocessed, template_preprocessed, cv2.TM_CCOEFF_NORMED)
    
    # Get locations where matches exceed threshold
    locations = np.where(result >= threshold)
    
    # If no matches, return empty list
    if len(locations[0]) == 0:
        return []
        
    # Find the best match (highest score)
    best_score = np.max(result)
    best_locations = np.where(result == best_score)
    
    # Convert to list of (x,y) tuples
    matches = list(zip(*best_locations[::-1]))
    
    return matches
