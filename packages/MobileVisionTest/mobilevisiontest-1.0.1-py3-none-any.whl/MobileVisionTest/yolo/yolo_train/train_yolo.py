import os
from inference import get_model
import supervision as sv
import cv2

def run_inference_roboflow(model_id, api_key, image_dir, output_dir):
    """
    Run inference using a Roboflow model and visualize with supervision.
    
    Args:
        model_id (str): Roboflow model ID (e.g., '6').
        api_key (str): Roboflow API key.
        image_dir (str): Directory containing input images.
        output_dir (str): Directory to save output images with bounding boxes.
    """
    # Load Roboflow model
    try:
        model = get_model(model_id=model_id, api_key=api_key)
    except Exception as e:
        print(f"Failed to load model: {e}")
        return
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize supervision annotators
    box_annotator = sv.BoxAnnotator()
    
    # Process each image
    for img_file in os.listdir(image_dir):
        if not img_file.endswith(('.png', '.jpg')):
            continue
        
        img_path = os.path.join(image_dir, img_file)
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load image: {img_path}")
            continue
        
        # Run inference
        try:
            results = model.infer(img_path)[0]  # Get first prediction
        except Exception as e:
            print(f"Inference failed for {img_file}: {e}")
            continue
        
        # Convert to supervision Detections
        detections = sv.Detections.from_inference(results)
        
        # Custom labels for visualization
        labels = [f"{det[3]} {det[2]:.2f}" for det in detections]
        
        # Annotate image
        annotated_img = box_annotator.annotate(scene=img.copy(), detections=detections)
        # Add text labels manually
        for label, (x, y, _, _) in zip(labels, detections.xyxy):
            cv2.putText(
                annotated_img,
                label,
                (int(x), int(y) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
        
        # Save output
        output_path = os.path.join(output_dir, f"annotated_{img_file}")
        cv2.imwrite(output_path, annotated_img)
        print(f"Saved annotated image: {output_path}")

# Example usage
if __name__ == "__main__":
    model_id = "mobile-vision-test/6"  # Replace with your model ID
    api_key = "PWV8XiuOgfZUPKKNhkwO"  # Replace with your API key
    image_dir = "screenshots"
    output_dir = "screen_output"
    run_inference_roboflow(model_id, api_key, image_dir, output_dir)