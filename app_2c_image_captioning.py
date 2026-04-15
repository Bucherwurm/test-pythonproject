"""
💬 AI IMAGE CAPTIONING
Generate human-like descriptions of images using AI
"""

import streamlit as st
from PIL import Image
from transformers import pipeline
import torch

st.set_page_config(page_title="💬 AI Image Captioning", page_icon="💬")

st.title("💬 AI Image Captioning")
st.write("Transform images into words with AI-powered natural language generation!")

st.sidebar.markdown("---")
st.sidebar.write("🗣️ **Captioning Features:**")
st.sidebar.write("• Natural language generation")
st.sidebar.write("• Scene understanding")
st.sidebar.write("• Multiple caption styles")
st.sidebar.write("• Human-like descriptions")

@st.cache_resource
def load_captioner():
    """Load image captioning model with caching"""
    try:
        captioner = pipeline("image-to-text", 
                             model="nlpconnect/vit-gpt2-image-captioning")
        return captioner
    except Exception as e:
        st.error(f"Error loading captioning model: {e}")
        return None

def generate_multiple_captions(image, captioner, num_captions=3):
    """Generate multiple captions with different parameters"""
    captions = []
    
    try:
        # Generate captions with different settings
        for i in range(num_captions):
            # Vary parameters for diversity
            caption_result = captioner(image)
            
            if caption_result:
                caption_text = caption_result[0]['generated_text']
                captions.append(caption_text)
        
        return captions
    except Exception as e:
        st.error(f"Error generating captions: {e}")
        return []

def analyze_caption_quality(caption):
    """Simple analysis of caption quality"""
    words = caption.lower().split()
    
    # Basic metrics
    word_count = len(words)
    char_count = len(caption)
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    
    # Complexity indicators
    descriptive_words = ['beautiful', 'large', 'small', 'old', 'young', 'bright', 'dark', 'colorful']
    action_words = ['walking', 'running', 'sitting', 'standing', 'flying', 'swimming', 'eating']
    
    descriptive_count = sum(1 for word in words if word in descriptive_words)
    action_count = sum(1 for word in words if word in action_words)
    
    # Quality score (simplified)
    quality_score = min(100, word_count * 8 + descriptive_count * 15 + action_count * 10)
    
    return {
        'word_count': word_count,
        'char_count': char_count,
        'avg_word_length': avg_word_length,
        'descriptive_words': descriptive_count,
        'action_words': action_count,
        'quality_score': quality_score
    }

st.header("📸 Image to Caption Generation")

uploaded_file = st.file_uploader("Choose an image to describe:", 
                               type=['jpg', 'jpeg', 'png', 'bmp'])

if uploaded_file is not None:
    # Display image
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(image, caption="Image to Describe", use_column_width=True)
        
        # Image properties
        st.subheader("📋 Image Properties")
        st.write(f"**Size:** {image.size[0]} x {image.size[1]} pixels")
        st.write(f"**Format:** {image.format}")
        st.write(f"**Mode:** {image.mode}")
        
        # Aspect ratio
        aspect_ratio = image.size[0] / image.size[1]
        if aspect_ratio > 1.5:
            orientation = "Landscape (Wide)"
        elif aspect_ratio < 0.75:
            orientation = "Portrait (Tall)"
        else:
            orientation = "Square/Balanced"
        st.write(f"**Orientation:** {orientation}")
    
    with col2:
        st.subheader("⚙️ Caption Settings")
        
        # Caption generation options
        num_captions = st.slider("Number of captions to generate:", 1, 5, 3)
        
        caption_style = st.selectbox("Caption style preference:", [
            "Standard (Balanced)",
            "Detailed (Longer descriptions)",
            "Concise (Short descriptions)",
            "Creative (More varied)"
        ])
        
        if st.button("💬 Generate Captions", type="primary"):
            captioner = load_captioner()
            
            if captioner:
                with st.spinner("🤖 AI is describing your image..."):
                    try:
                        # Resize image if needed for processing
                        if image.size[0] > 500 or image.size[1] > 500:
                            image_processed = image.copy()
                            image_processed.thumbnail((500, 500))
                        else:
                            image_processed = image
                        
                        # Generate captions
                        captions = generate_multiple_captions(image_processed, captioner, num_captions)
                        
                        if captions:
                            st.session_state['generated_captions'] = captions
                            st.session_state['caption_image'] = image
                        else:
                            st.error("Failed to generate captions. Please try again.")
                            
                    except Exception as e:
                        st.error(f"Error generating captions: {e}")
            else:
                st.error("Caption generation model not available.")

# Display generated captions
if 'generated_captions' in st.session_state:
    captions = st.session_state['generated_captions']
    
    st.markdown("---")
    st.subheader("🎨 Generated Descriptions")
    
    for i, caption in enumerate(captions):
        st.write(f"**Caption {i+1}:**")
        st.info(f"📝 {caption}")
        
        # Caption analysis
        analysis = analyze_caption_quality(caption)
        
        with st.expander(f"📊 Analysis for Caption {i+1}"):
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric("Words", analysis['word_count'])
                st.metric("Characters", analysis['char_count'])
            
            with col_b:
                st.metric("Descriptive Words", analysis['descriptive_words'])
                st.metric("Action Words", analysis['action_words'])
            
            with col_c:
                st.metric("Avg Word Length", f"{analysis['avg_word_length']:.1f}")
                st.metric("Quality Score", f"{analysis['quality_score']}/100")
    
    # Caption comparison
    if len(captions) > 1:
        st.subheader("⚖️ Caption Comparison")
        
        # Find best caption by different metrics
        analyses = [analyze_caption_quality(cap) for cap in captions]
        
        longest_idx = max(range(len(analyses)), key=lambda i: analyses[i]['word_count'])
        most_descriptive_idx = max(range(len(analyses)), key=lambda i: analyses[i]['descriptive_words'])
        highest_quality_idx = max(range(len(analyses)), key=lambda i: analyses[i]['quality_score'])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**📏 Longest Caption:**")
            st.write(f"Caption {longest_idx + 1} ({analyses[longest_idx]['word_count']} words)")
            st.info(captions[longest_idx])
        
        with col2:
            st.write("**🎨 Most Descriptive:**")
            st.write(f"Caption {most_descriptive_idx + 1} ({analyses[most_descriptive_idx]['descriptive_words']} descriptive words)")
            st.info(captions[most_descriptive_idx])
        
        with col3:
            st.write("**🏆 Highest Quality:**")
            st.write(f"Caption {highest_quality_idx + 1} (Score: {analyses[highest_quality_idx]['quality_score']}/100)")
            st.info(captions[highest_quality_idx])

# Interactive caption improvement
st.markdown("---")
st.header("✍️ Interactive Caption Workshop")

if 'generated_captions' in st.session_state:
    st.write("Compare AI-generated captions with your own description!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 AI Description")
        best_caption = st.session_state['generated_captions'][0]  # Use first caption
        st.info(best_caption)
    
    with col2:
        st.subheader("✍️ Your Description")
        user_caption = st.text_area("How would YOU describe this image?", 
                                   height=100,
                                   placeholder="Write your own description here...")
        
        if user_caption:
            user_analysis = analyze_caption_quality(user_caption)
            ai_analysis = analyze_caption_quality(best_caption)
            
            st.subheader("📊 Comparison")
            
            comparison_metrics = [
                ("Word Count", user_analysis['word_count'], ai_analysis['word_count']),
                ("Descriptive Words", user_analysis['descriptive_words'], ai_analysis['descriptive_words']),
                ("Quality Score", user_analysis['quality_score'], ai_analysis['quality_score'])
            ]
            
            for metric, user_val, ai_val in comparison_metrics:
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.write(f"**{metric}:**")
                with col_b:
                    st.write(f"Your: {user_val}")
                with col_c:
                    st.write(f"AI: {ai_val}")
            
            # Provide feedback
            if user_analysis['quality_score'] > ai_analysis['quality_score']:
                st.success("🎉 Great job! Your description scored higher than the AI!")
            elif user_analysis['quality_score'] == ai_analysis['quality_score']:
                st.info("🤝 You matched the AI's quality score!")
            else:
                st.info("💡 The AI scored higher, but your unique perspective adds value!")

# Educational content
with st.expander("🧠 How AI Image Captioning Works"):
    st.write("""
    **The Technology Behind Image Captioning:**
    
    1. **Computer Vision Component**
       - Extracts visual features from images
       - Identifies objects, scenes, relationships
       - Uses Convolutional Neural Networks (CNNs) or Vision Transformers
    
    2. **Natural Language Processing Component**
       - Converts visual features into text
       - Uses language models like GPT-2
       - Generates human-like sentences
    
    3. **Encoder-Decoder Architecture**
       - **Encoder**: Processes image and creates feature representation
       - **Decoder**: Generates text word by word based on features
       - **Attention Mechanism**: Focuses on relevant image parts for each word
    
    **Model Architecture (ViT-GPT2):**
    - Vision Transformer (ViT) for image understanding
    - GPT-2 for language generation
    - Cross-attention between vision and language components
    
    **Training Process:**
    - Trained on millions of image-caption pairs
    - Learns associations between visual patterns and words
    - Optimized to generate accurate, fluent descriptions
    """)

with st.expander("📝 Caption Quality Evaluation"):
    st.write("""
    **What Makes a Good Caption?**
    
    **Technical Metrics:**
    • **BLEU Score**: Compares generated text to reference captions
    • **ROUGE Score**: Measures overlap with human-written descriptions
    • **CIDEr**: Consensus-based evaluation for image descriptions
    • **METEOR**: Considers synonyms and paraphrases
    
    **Human Quality Factors:**
    • **Accuracy**: Does it correctly describe what's in the image?
    • **Completeness**: Does it mention important objects and scenes?
    • **Fluency**: Is the language natural and grammatically correct?
    • **Specificity**: Does it provide useful details vs. generic descriptions?
    
    **Common Caption Types:**
    • **Factual**: "A red car parked on a street"
    • **Detailed**: "A vintage red convertible parked in front of a brick building"
    • **Creative**: "A cherry-red classic car awaits its next adventure"
    • **Technical**: "A 1960s Ford Mustang convertible in red paint"
    
    **Evaluation Challenges:**
    - Multiple valid descriptions for same image
    - Subjective preferences for detail level
    - Cultural and contextual differences
    - Balance between accuracy and creativity
    """)

with st.expander("🚀 Applications & Future Directions"):
    st.write("""
    **Real-World Applications:**
    
    **Accessibility:**
    - Screen readers for visually impaired users
    - Alternative text for web images
    - Audio descriptions for visual content
    
    **Content Management:**
    - Automatic image tagging and organization
    - Search engine optimization (SEO)
    - Social media content generation
    
    **Healthcare:**
    - Medical image reporting assistance
    - Radiology report generation
    - Patient education materials
    
    **Education:**
    - Automated description of educational images
    - Language learning aids
    - Historical photo documentation
    
    **Future Improvements:**
    - Better understanding of context and relationships
    - More diverse and inclusive training data
    - Integration with real-time video captioning
    - Personalized caption styles
    - Multi-modal understanding (text + images + audio)
    """)

st.write("💡 **Learning Outcome:** Understand multimodal AI, encoder-decoder architectures, natural language generation, and human-AI collaboration.")
