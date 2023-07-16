import cv2
import numpy as np
class ClusterManager:

    width = None
    height = None

    thresh1 = 95
    thresh2 = 150

    min_area = 750
    max_area = 2250

    centroid_grid = None

    last_unfiltered = None

    def __init__(self, frame_width, frame_height, t1=95, t2=150, min_area=750, max_area=2250):
        ClusterManager.width = frame_width
        ClusterManager.height = frame_height

        ClusterManager.thresh1 = t1
        ClusterManager.thresh2 = t2

        ClusterManager.min_area = min_area
        ClusterManager.max_area = max_area

    @classmethod
    def filter_contours(cls, frame, contour_mode=cv2.RETR_TREE, contour_method=cv2.CHAIN_APPROX_NONE):
    
        contours, hierarchy = cv2.findContours(frame, mode=contour_mode, method=contour_method)

        cls.last_unfiltered = contours
        filtered_contours = None
        for contour in contours:
            area = cv2.contourArea(contour)

            # If in size range
            if area < cls.max_area and area > cls.min_area:

                # Initilize np.array for storing contours within size range
                if filtered_contours is None: filtered_contours = np.array(contour)

                # If np.array already initalized append current contour
                else: filtered_contours = np.append(filtered_contours, contour, axis=0)

        if filtered_contours is None:
            return None
        
        return filtered_contours.reshape((-1, 2)), filtered_contours

    @classmethod
    def init_centroids(cls, width_count=4, height_count=4):
        centroids = []
        width_bins = 4
        height_bins = 4
        
        x_diff = cls.width // width_bins
        y_diff = cls.height // height_bins
        curr_y = y_diff
        
        for _ in range(height_bins-1):
            curr_x = x_diff
            for _ in range(width_bins-1):
                centroids.append([curr_x, curr_y])
                curr_x += x_diff
            curr_y += y_diff
        
        cls.centroid_grid = np.array(centroids)
    
    @classmethod
    def update_centroid(cls, X, indicies, K):
        m, n = X.shape
        new_centroids = []

        # For each centroid
        for k in range(K):

            # Find all points bound to the current centroid
            points = X[indicies==k]

            # If there is at least one point
            if len(points) != 0:
                new_centroids.append(np.mean(points, axis=0))
        return np.array(new_centroids)
    
    @classmethod
    def find_closest_centroid(cls, X, centroids):
        K = centroids.shape[0]
        m, n = X.shape

        indices = np.zeros(m, dtype=int)

        # For each point
        for i in range(m):
            distances = []

            # For each centroids
            for j in range(K):

                # Calc distance
                norm = np.linalg.norm(X[i] - centroids[j], axis=0)
                distances.append(norm)

            # Save min distance to current point
            indices[i] = np.argmin(distances)

        return indices
    
    @classmethod
    def kmeans(cls, points, max_iter=5, debug=False):

        if cls.centroid_grid is None: 
            cls.init_centroids()
    
        centroids = cls.centroid_grid

        m, n = centroids.shape
        indicies = np.zeros(m)

        for i in range(max_iter):
            K = len(centroids)
            if debug: print(f"\n\nK-Means Iteration ({i}) / ({max_iter})")
            indicies = cls.find_closest_centroid(points, centroids)
            centroids = cls.update_centroid(points, indicies, K)

        return centroids

    @classmethod
    def capture_subimages(cls, frame, centroids, subframe_width=150, subframe_height=150):
        subimages = []

        for centroid in centroids:
            centroid_x, centroid_y = tuple(np.uint32(centroid))
            x1 = max(centroid_x - subframe_width//2, 0)
            x2 = min(centroid_x + subframe_width//2, cls.width)
            y1 = max(centroid_y - subframe_height//2, 0)
            y2 = min(centroid_y + subframe_height//2, cls.height)

            subimages.append(frame[y1:y2, x1:x2])

        return subimages
