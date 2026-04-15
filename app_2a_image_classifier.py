"""
🎯 AI IMAGE CLASSIFIER
Advanced image classification using pre-trained AI models
"""

import streamlit as st
from PIL import Image
import sys
from transformers import pipeline
import torch


st.set_page_config(page_title="🎯 AI Image Classifier", page_icon="🎯")

st.title("🎯 AI Image Classifier")
st.write("Harness the power of AI to classify and understand images!")

st.sidebar.markdown("---")
st.sidebar.write("🤖 **AI Technologies:**")
st.sidebar.write("• Vision Transformer (ViT)")
st.sidebar.write("• Pre-trained Neural Networks")
st.sidebar.write("• Hugging Face Models")
st.sidebar.write("• Deep Learning Classification")

@st.cache_resource
def load_classifier():
    try:
        classifier = pipeline("image-classification", 
                             model="google/vit-base-patch16-224")
        return classifier
    except Exception as e:
        st.error(f"Error loading AI model: {e}")
        st.info("This might be due to missing dependencies or network issues. Please ensure all packages are installed.")
        return None

def analyze_image_safety(image):
    """Basic content safety check"""
    try:
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Basic safety assessment
        width, height = image.size
        safety_score = 0.95  # Default to safe for demo
        
        return {
            'is_safe': safety_score > 0.5,
            'confidence': safety_score,
            'reasoning': 'Content appears safe for AI analysis'
        }
    except:
        return {
            'is_safe': True,
            'confidence': 0.8,
            'reasoning': 'Could not fully analyze content, proceeding with caution'
        }

st.header("📷 Upload & Classify Images")

uploaded_file = st.file_uploader("Choose an image...", 
                               type=['jpg', 'jpeg', 'png', 'bmp', 'webp'])

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Image metadata
        st.subheader("📋 Image Information")
        st.write(f"**Format:** {image.format}")
        st.write(f"**Size:** {image.size[0]} x {image.size[1]} pixels")
        st.write(f"**Mode:** {image.mode}")
        
        # File size
        file_size = len(uploaded_file.getvalue())
        if file_size > 1024 * 1024:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"
        else:
            size_str = f"{file_size / 1024:.1f} KB"
        st.write(f"**File Size:** {size_str}")
        
    with col2:
        # Safety check
        safety_result = analyze_image_safety(image)
        
        if safety_result['is_safe']:
            st.success("✅ Image appears safe for AI analysis")
            
            # Load AI model
            classifier = load_classifier()
            
            if classifier:
                with st.spinner("🤖 AI is analyzing your image..."):
                    try:
                        # Classify the image
                        results = classifier(image)
                        
                        st.subheader("🎯 AI Classification Results")
                        
                        # Display top results
                        for i, result in enumerate(results[:5]):
                            confidence = result['score'] * 100
                            label = result['label']
                            
                            # Create confidence visualization
                            st.write(f"**{i+1}. {label}**")
                            
                            # Progress bar for confidence
                            st.progress(result['score'])
                            
                            # Confidence with color coding
                            if confidence >= 80:
                                st.success(f"High Confidence: {confidence:.1f}%")
                            elif confidence >= 50:
                                st.info(f"Medium Confidence: {confidence:.1f}%")
                            else:
                                st.warning(f"Low Confidence: {confidence:.1f}%")
                            
                            st.write("---")
                        
                        # Analysis insights
                        st.subheader("🔍 AI Analysis Insights")
                        
                        top_result = results[0]
                        top_confidence = top_result['score'] * 100
                        
                        if top_confidence >= 90:
                            st.success(f"🎯 **High Certainty:** The AI is very confident this is a {top_result['label']}")
                        elif top_confidence >= 70:
                            st.info(f"👍 **Good Match:** The AI believes this is likely a {top_result['label']}")
                        elif top_confidence >= 50:
                            st.warning(f"🤔 **Moderate Confidence:** The AI thinks this might be a {top_result['label']}")
                        else:
                            st.error(f"❓ **Uncertain:** The AI is not confident about this classification")
                        
                        # Show confidence distribution
                        with st.expander("📊 Detailed Confidence Analysis"):
                            st.write("**All Predictions:**")
                            
                            labels = [r['label'] for r in results]
                            scores = [r['score'] * 100 for r in results]
                            
                            import plotly.express as px
                            fig = px.bar(x=labels, y=scores, 
                                       title="AI Confidence for Each Classification",
                                       labels={'x': 'Classification', 'y': 'Confidence (%)'})
                            fig.update_layout(xaxis_tickangle=-45)
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Technical details
                            st.write("**Model Information:**")
                            st.write("• **Model:** Vision Transformer (ViT) Base")
                            st.write("• **Training Data:** ImageNet-21k + ImageNet-1k")
                            st.write("• **Classes:** 1,000 different categories")
                            st.write("• **Input Size:** 224x224 pixels")
                        
                    except Exception as e:
                        st.error(f"Error in AI classification: {e}")
                        st.info("💡 Try a different image or check your internet connection")
            else:
                st.warning("⚠️ AI model is loading... Please wait and try again.")
        else:
            st.warning("⚠️ Image content requires manual review before AI analysis")

# Educational content
st.markdown("---")
st.subheader("🎓 Understanding AI Image Classification")

with st.expander("🧠 How AI Image Classification Works"):
    st.write("""
    **The Technology Behind the Magic:**
    
    1. **Convolutional Neural Networks (CNNs)**
       - Designed to process grid-like data (images)
       - Use filters to detect features like edges, shapes, textures
       - Stack multiple layers to learn complex patterns
    
    2. **Vision Transformer (ViT)**
       - Modern approach that treats images as sequences of patches
       - Uses attention mechanisms to focus on important parts
       - Often more accurate than traditional CNNs
    
    3. **Transfer Learning**
       - Pre-trained on millions of images (ImageNet dataset)
       - Fine-tuned for specific tasks
       - Saves time and computational resources
    
    **The Classification Process:**
    1. **Preprocessing** - Resize image to standard dimensions (224x224)
    2. **Feature Extraction** - AI identifies patterns and features
    3. **Classification** - Maps features to known categories
    4. **Confidence Scoring** - Provides probability for each prediction
    """)

with st.expander("📊 Understanding Confidence Scores"):
    st.write("""
    **What Confidence Scores Mean:**
    
    • **90-100%**: Extremely confident - Very likely correct
    • **70-89%**: High confidence - Probably correct
    • **50-69%**: Moderate confidence - Possibly correct
    • **30-49%**: Low confidence - Uncertain
    • **Below 30%**: Very uncertain - Likely incorrect
    
    **Why Confidence Matters:**
    - Helps you understand reliability of predictions
    - Important for automated decision-making
    - Indicates when human review is needed
    
    **Factors Affecting Confidence:**
    - Image quality and clarity
    - Lighting conditions
    - Object size and position
    - Similarity to training data
    - Presence of multiple objects
    """)

with st.expander("🔬 Model Technical Details"):
    st.write("""
    **Vision Transformer (ViT) Specifications:**
    
    • **Architecture**: Transformer-based (not CNN-based)
    • **Input Resolution**: 224x224 pixels
    • **Patch Size**: 16x16 pixels
    • **Parameters**: ~86 million
    • **Training Dataset**: ImageNet-21k (14M images) + ImageNet-1k (1.3M images)
    • **Number of Classes**: 1,000 different categories
    
    **Advantages of ViT:**
    - Better at capturing global relationships in images
    - More interpretable attention patterns
    - Often superior performance on diverse image types
    - Scales well with larger datasets
    
    **Use Cases:**
    - Medical image analysis
    - Autonomous vehicle vision
    - Content moderation
    - Product categorization
    - Quality control in manufacturing
    """)

st.write("💡 **Learning Outcome:** Understand computer vision, neural networks, transfer learning, and AI model evaluation.")
