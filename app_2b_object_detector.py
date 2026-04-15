"""
🔍 OBJECT DETECTION STUDIO
Advanced object detection and localization in images
"""
# pip install timm transformers torch streamlit
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline
import torch

st.set_page_config(page_title="🔍 Object Detection Studio", page_icon="🔍")

st.title("🔍 Object Detection Studio")
st.write("Detect and locate multiple objects in images with AI precision!")

st.sidebar.markdown("---")
st.sidebar.write("🎯 **Detection Features:**")
st.sidebar.write("• Multi-object detection")
st.sidebar.write("• Bounding box visualization")
st.sidebar.write("• Confidence scoring")
st.sidebar.write("• Object counting")

@st.cache_resource
def load_detector():
    """Load object detection model with caching"""
    try:
        detector = pipeline("object-detection", 
                           model="facebook/detr-resnet-50")
        return detector
    except Exception as e:
        st.error(f"Error loading detection model: {e}")
        return None

def draw_bounding_boxes(image, detections, min_confidence=0.5):
    """Draw bounding boxes on image"""
    # Create a copy of the image
    img_with_boxes = image.copy()
    draw = ImageDraw.Draw(img_with_boxes)
    
    # Color palette for different objects
    colors = [
        '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF',
        '#FFA500', '#800080', '#FFC0CB', '#A52A2A', '#808080', '#000000'
    ]
    
    valid_detections = []
    
    for i, detection in enumerate(detections):
        confidence = detection['score']
        
        if confidence >= min_confidence:
            box = detection['box']
            label = detection['label']
            
            # Get color for this detection
            color = colors[i % len(colors)]
            
            # Draw bounding box
            x1, y1, x2, y2 = box['xmin'], box['ymin'], box['xmax'], box['ymax']
            draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
            
            # Draw label background
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            label_text = f"{label} ({confidence:.1%})"
            
            # Get text bounding box
            bbox = draw.textbbox((x1, y1), label_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Draw background rectangle for text
            draw.rectangle([x1, y1-text_height-4, x1+text_width+4, y1], fill=color)
            
            # Draw text
            draw.text((x1+2, y1-text_height-2), label_text, fill='white', font=font)
            
            valid_detections.append(detection)
    
    return img_with_boxes, valid_detections

st.header("📷 Object Detection Analysis")

uploaded_file = st.file_uploader("Choose an image for object detection:", 
                               type=['jpg', 'jpeg', 'png', 'bmp'])

if uploaded_file is not None:
    # Load and display image
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📷 Original Image")
        st.image(image, caption="Input Image", use_column_width=True)
        
        # Image info
        st.write(f"**Dimensions:** {image.size[0]} x {image.size[1]} pixels")
        st.write(f"**Format:** {image.format}")
        
    with col2:
        st.subheader("⚙️ Detection Settings")
        
        # Confidence threshold
        min_confidence = st.slider(
            "Minimum confidence threshold:",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.05
        )
        
        # Detection button
        if st.button("🔍 Detect Objects", type="primary"):
            detector = load_detector()
            
            if detector:
                with st.spinner("🕵️ AI is detecting objects..."):
                    try:
                        # Resize image if too large for faster processing
                        if image.size[0] > 800 or image.size[1] > 800:
                            image_resized = image.copy()
                            image_resized.thumbnail((800, 800))
                        else:
                            image_resized = image
                        
                        # Perform object detection
                        detections = detector(image_resized)
                        
                        # Store results in session state
                        st.session_state['detections'] = detections
                        st.session_state['detection_image'] = image_resized
                        
                    except Exception as e:
                        st.error(f"Error in object detection: {e}")
            else:
                st.error("Object detection model not available.")

# Display detection results
if 'detections' in st.session_state:
    detections = st.session_state['detections']
    detection_image = st.session_state['detection_image']
    
    # Filter detections by confidence
    filtered_detections = [d for d in detections if d['score'] >= min_confidence]
    
    st.markdown("---")
    st.subheader(f"🎯 Detection Results ({len(filtered_detections)} objects found)")
    
    if filtered_detections:
        # Draw bounding boxes
        img_with_boxes, valid_detections = draw_bounding_boxes(
            detection_image, filtered_detections, min_confidence
        )
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image(img_with_boxes, caption="Detected Objects", use_column_width=True)
        
        with col2:
            st.subheader("📋 Detected Objects")
            
            # Object summary
            object_counts = {}
            for detection in valid_detections:
                label = detection['label']
                object_counts[label] = object_counts.get(label, 0) + 1
            
            # Display object counts
            for obj, count in sorted(object_counts.items()):
                st.write(f"🎯 **{obj}**: {count}")
            
            # Summary metrics
            st.subheader("📊 Detection Summary")
            
            total_objects = len(valid_detections)
            avg_confidence = sum(d['score'] for d in valid_detections) / len(valid_detections) if valid_detections else 0
            high_confidence = len([d for d in valid_detections if d['score'] > 0.8])
            
            st.metric("Total Objects", total_objects)
            st.metric("Average Confidence", f"{avg_confidence:.1%}")
            st.metric("High Confidence (>80%)", high_confidence)
        
        # Detailed detection list
        st.subheader("📝 Detailed Detection List")
        
        for i, detection in enumerate(valid_detections):
            with st.expander(f"Object {i+1}: {detection['label']} ({detection['score']:.1%})"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.write(f"**Label:** {detection['label']}")
                    st.write(f"**Confidence:** {detection['score']:.1%}")
                    
                with col_b:
                    box = detection['box']
                    st.write(f"**Bounding Box:**")
                    st.write(f"• Top-left: ({box['xmin']:.0f}, {box['ymin']:.0f})")
                    st.write(f"• Bottom-right: ({box['xmax']:.0f}, {box['ymax']:.0f})")
                    
                    # Calculate box dimensions
                    width = box['xmax'] - box['xmin']
                    height = box['ymax'] - box['ymin']
                    area = width * height
                    
                    st.write(f"**Dimensions:**")
                    st.write(f"• Width: {width:.0f}px")
                    st.write(f"• Height: {height:.0f}px")
                    st.write(f"• Area: {area:.0f}px²")
        
        # Advanced analysis
        st.subheader("🔬 Advanced Analysis")
        
        # Object size analysis
        sizes = []
        for detection in valid_detections:
            box = detection['box']
            width = box['xmax'] - box['xmin']
            height = box['ymax'] - box['ymin']
            area = width * height
            sizes.append(area)
        
        if sizes:
            import plotly.express as px
            import pandas as pd
            
            # Create size distribution chart
            size_df = pd.DataFrame({
                'Object': [f"{d['label']} {i+1}" for i, d in enumerate(valid_detections)],
                'Area (pixels²)': sizes,
                'Confidence': [d['score'] for d in valid_detections]
            })
            
            fig = px.scatter(size_df, x='Area (pixels²)', y='Confidence',
                           hover_data=['Object'],
                           title="Object Size vs Confidence",
                           labels={'Confidence': 'Detection Confidence'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Confidence distribution
            confidence_scores = [d['score'] for d in valid_detections]
            fig2 = px.histogram(x=confidence_scores, nbins=10,
                              title="Confidence Score Distribution",
                              labels={'x': 'Confidence Score', 'y': 'Number of Objects'})
            st.plotly_chart(fig2, use_container_width=True)
    
    else:
        st.warning(f"No objects detected with confidence ≥ {min_confidence:.0%}. Try lowering the confidence threshold.")

# Comparison mode
st.markdown("---")
st.header("⚖️ Detection Comparison Mode")

st.write("Compare object detection results with different confidence thresholds:")

if 'detections' in st.session_state:
    col1, col2, col3 = st.columns(3)
    
    thresholds = [0.3, 0.5, 0.8]
    
    for i, threshold in enumerate(thresholds):
        with [col1, col2, col3][i]:
            st.subheader(f"Threshold: {threshold:.0%}")
            
            filtered = [d for d in st.session_state['detections'] if d['score'] >= threshold]
            
            if filtered:
                img_with_boxes, _ = draw_bounding_boxes(
                    st.session_state['detection_image'], filtered, threshold
                )
                st.image(img_with_boxes, use_column_width=True)
                st.write(f"**Objects found:** {len(filtered)}")
            else:
                st.write("No objects detected at this threshold")

# Educational content
st.markdown("---")
st.subheader("🎓 Understanding Object Detection")

with st.expander("🧠 How Object Detection Works"):
    st.write("""
    **Object Detection vs Image Classification:**
    
    • **Image Classification**: "What is in this image?" (one answer)
    • **Object Detection**: "What objects are where in this image?" (multiple answers with locations)
    
    **The Detection Process:**
    
    1. **Feature Extraction**
       - Extract visual features from the entire image
       - Use convolutional neural networks (CNNs)
    
    2. **Region Proposal**
       - Identify potential object locations
       - Generate bounding box candidates
    
    3. **Classification & Localization**
       - Classify what's in each bounding box
       - Refine the box coordinates
    
    4. **Non-Maximum Suppression**
       - Remove duplicate detections
       - Keep only the best detection per object
    
    **DETR (Detection Transformer):**
    - Modern approach using transformer architecture
    - Predicts bounding boxes and classes directly
    - No need for manual region proposals
    """)

with st.expander("📊 Understanding Bounding Boxes"):
    st.write("""
    **Bounding Box Coordinates:**
    
    • **xmin, ymin**: Top-left corner coordinates
    • **xmax, ymax**: Bottom-right corner coordinates
    • **Width**: xmax - xmin
    • **Height**: ymax - ymin
    • **Area**: width × height
    
    **Coordinate System:**
    - Origin (0,0) is at the top-left of the image
    - X increases going right
    - Y increases going down
    
    **Box Quality Metrics:**
    - **Intersection over Union (IoU)**: Measures box accuracy
    - **Aspect Ratio**: Width/height ratio
    - **Coverage**: Percentage of image area covered
    
    **Common Issues:**
    - **Over-detection**: Same object detected multiple times
    - **Under-detection**: Missing objects that should be detected
    - **Misclassification**: Wrong label for detected object
    - **Poor localization**: Correct detection but wrong box position
    """)

with st.expander("🎯 Confidence Thresholds & Performance"):
    st.write("""
    **Choosing the Right Threshold:**
    
    • **Low Threshold (0.1-0.3)**
       - Catches more objects (high recall)
       - More false positives
       - Good for not missing anything important
    
    • **Medium Threshold (0.4-0.6)**
       - Balanced precision and recall
       - Good for general use cases
       - Reasonable trade-off
    
    • **High Threshold (0.7-0.9)**
       - High precision, fewer false positives
       - Might miss some objects (low recall)
       - Good when accuracy is critical
    
    **Performance Metrics:**
    - **Precision**: How many detections are correct?
    - **Recall**: How many actual objects were detected?
    - **F1-Score**: Harmonic mean of precision and recall
    - **mAP**: Mean Average Precision (standard evaluation metric)
    
    **Real-world Applications:**
    - **Autonomous Vehicles**: High threshold for safety
    - **Surveillance**: Medium threshold for balance
    - **Medical Imaging**: Low threshold to not miss anything
    """)

st.write("💡 **Learning Outcome:** Understand object detection algorithms, bounding box representation, confidence thresholds, and performance evaluation.")
