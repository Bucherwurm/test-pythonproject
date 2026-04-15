"""
📊 AI VISION ANALYTICS
Comprehensive image analysis combining multiple AI techniques
"""

import streamlit as st
from PIL import Image
import io
from transformers import pipeline
import torch
import plotly.express as px
import pandas as pd
from collections import Counter

st.set_page_config(page_title="📊 AI Vision Analytics", page_icon="📊", layout="wide")

st.title("📊 AI Vision Analytics")
st.write("Complete image analysis combining classification, detection, and captioning!")

st.sidebar.markdown("---")
st.sidebar.write("🔬 **Analytics Features:**")
st.sidebar.write("• Multi-model analysis")
st.sidebar.write("• Comprehensive reporting")
st.sidebar.write("• Visual insights")
st.sidebar.write("• Performance comparison")

@st.cache_resource
def load_all_models():
    """Load all AI models with caching"""
    models = {}
    
    try:
        models['classifier'] = pipeline("image-classification", 
                                      model="google/vit-base-patch16-224")
    except Exception as e:
        st.warning(f"Could not load classifier: {e}")
        models['classifier'] = None
    
    try:
        models['detector'] = pipeline("object-detection", 
                                    model="facebook/detr-resnet-50")
    except Exception as e:
        st.warning(f"Could not load detector: {e}")
        models['detector'] = None
    
    try:
        models['captioner'] = pipeline("image-to-text", 
                                     model="nlpconnect/vit-gpt2-image-captioning")
    except Exception as e:
        st.warning(f"Could not load captioner: {e}")
        models['captioner'] = None
    
    return models

def perform_comprehensive_analysis(image, models):
    """Perform complete image analysis using all available models"""
    results = {}
    
    # Prepare image for processing
    if image.size[0] > 800 or image.size[1] > 800:
        image_processed = image.copy()
        image_processed.thumbnail((800, 800))
    else:
        image_processed = image
    
    # Classification Analysis
    if models['classifier']:
        try:
            classification_results = models['classifier'](image_processed)
            results['classification'] = classification_results
        except Exception as e:
            st.error(f"Classification error: {e}")
            results['classification'] = None
    
    # Object Detection Analysis
    if models['detector']:
        try:
            detection_results = models['detector'](image_processed)
            results['detection'] = detection_results
        except Exception as e:
            st.error(f"Detection error: {e}")
            results['detection'] = None
    
    # Caption Generation
    if models['captioner']:
        try:
            caption_results = models['captioner'](image_processed)
            results['caption'] = caption_results[0]['generated_text'] if caption_results else None
        except Exception as e:
            st.error(f"Captioning error: {e}")
            results['caption'] = None
    
    return results

def create_analysis_report(image, results):
    """Create comprehensive analysis report"""
    report = {
        'image_properties': {
            'width': image.size[0],
            'height': image.size[1],
            'aspect_ratio': image.size[0] / image.size[1],
            'format': image.format,
            'mode': image.mode
        },
        'analysis_summary': {},
        'confidence_scores': {},
        'object_counts': {},
        'scene_description': None
    }
    
    # Process classification results
    if results.get('classification'):
        top_class = results['classification'][0]
        report['analysis_summary']['primary_classification'] = top_class['label']
        report['confidence_scores']['classification_confidence'] = top_class['score']
        
        # Get all classifications above threshold
        high_confidence_classes = [
            r for r in results['classification'] 
            if r['score'] > 0.1
        ]
        report['analysis_summary']['all_classifications'] = len(high_confidence_classes)
    
    # Process detection results
    if results.get('detection'):
        detections = results['detection']
        report['analysis_summary']['objects_detected'] = len(detections)
        
        # Count objects by type
        object_types = [d['label'] for d in detections]
        report['object_counts'] = dict(Counter(object_types))
        
        # Average detection confidence
        if detections:
            avg_detection_confidence = sum(d['score'] for d in detections) / len(detections)
            report['confidence_scores']['avg_detection_confidence'] = avg_detection_confidence
    
    # Process caption
    if results.get('caption'):
        report['scene_description'] = results['caption']
        report['analysis_summary']['caption_length'] = len(results['caption'].split())
    
    return report

st.header("🔍 Comprehensive Image Analysis")

uploaded_file = st.file_uploader("Upload an image for complete AI analysis:", 
                               type=['jpg', 'jpeg', 'png', 'bmp'])

if uploaded_file is not None:
    # Load image
    image = Image.open(uploaded_file)
    
    # Display image
    st.subheader("📷 Input Image")
    st.image(image, caption="Image for Analysis", use_column_width=True)
    
    # Analysis button
    if st.button("🚀 Perform Complete Analysis", type="primary"):
        # Load models
        models = load_all_models()
        
        # Check if any models are available
        available_models = [name for name, model in models.items() if model is not None]
        
        if available_models:
            st.info(f"Available AI models: {', '.join(available_models)}")
            
            with st.spinner("🤖 Performing comprehensive AI analysis..."):
                # Perform analysis
                results = perform_comprehensive_analysis(image, models)
                
                # Generate report
                report = create_analysis_report(image, results)
                
                # Store in session state
                st.session_state['analysis_results'] = results
                st.session_state['analysis_report'] = report
                st.session_state['analyzed_image'] = image
                
                st.success("✅ Analysis complete!")
        else:
            st.error("No AI models available for analysis.")

# Display analysis results
if 'analysis_results' in st.session_state:
    results = st.session_state['analysis_results']
    report = st.session_state['analysis_report']
    
    st.markdown("---")
    st.header("📊 Analysis Dashboard")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if results.get('classification'):
            top_class = results['classification'][0]['label']
            confidence = results['classification'][0]['score'] * 100
            st.metric("Primary Classification", top_class, f"{confidence:.1f}% confidence")
        else:
            st.metric("Primary Classification", "N/A")
    
    with col2:
        objects_detected = len(results.get('detection', []))
        st.metric("Objects Detected", objects_detected)
    
    with col3:
        if results.get('caption'):
            caption_words = len(results['caption'].split())
            st.metric("Caption Words", caption_words)
        else:
            st.metric("Caption Words", "N/A")
    
    with col4:
        # Overall analysis score
        scores = []
        if results.get('classification'):
            scores.append(results['classification'][0]['score'])
        if results.get('detection'):
            avg_det_score = sum(d['score'] for d in results['detection']) / len(results['detection'])
            scores.append(avg_det_score)
        
        overall_score = sum(scores) / len(scores) * 100 if scores else 0
        st.metric("Overall Confidence", f"{overall_score:.1f}%")
    
    # Detailed results in tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Classification", "🔍 Object Detection", "💬 Scene Description", "📈 Analytics"])
    
    with tab1:
        if results.get('classification'):
            st.subheader("🎯 Image Classification Results")
            
            # Top classifications
            for i, result in enumerate(results['classification'][:5]):
                confidence = result['score'] * 100
                label = result['label']
                
                col_a, col_b = st.columns([3, 1])
                
                with col_a:
                    st.write(f"**{i+1}. {label}**")
                    st.progress(result['score'])
                
                with col_b:
                    if confidence >= 70:
                        st.success(f"{confidence:.1f}%")
                    elif confidence >= 40:
                        st.info(f"{confidence:.1f}%")
                    else:
                        st.warning(f"{confidence:.1f}%")
            
            # Classification confidence chart
            class_data = pd.DataFrame(results['classification'][:8])
            fig = px.bar(class_data, x='label', y='score',
                        title='Classification Confidence Scores',
                        labels={'score': 'Confidence', 'label': 'Classification'})
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Classification analysis not available.")
    
    with tab2:
        if results.get('detection'):
            st.subheader("🔍 Object Detection Results")
            
            detections = results['detection']
            
            # Object summary
            object_counts = Counter([d['label'] for d in detections])
            
            st.write("**Objects Found:**")
            for obj, count in object_counts.most_common():
                st.write(f"• **{obj}**: {count}")
            
            # Detection details
            st.subheader("📋 Detailed Detections")
            
            detection_data = []
            for i, detection in enumerate(detections):
                detection_data.append({
                    'Object': detection['label'],
                    'Confidence': f"{detection['score']:.1%}",
                    'Box Area': (detection['box']['xmax'] - detection['box']['xmin']) * 
                               (detection['box']['ymax'] - detection['box']['ymin']),
                    'X': detection['box']['xmin'],
                    'Y': detection['box']['ymin']
                })
            
            detection_df = pd.DataFrame(detection_data)
            st.dataframe(detection_df)
            
            # Object size vs confidence scatter plot
            if len(detection_data) > 1:
                fig = px.scatter(detection_df, x='Box Area', y='Confidence',
                               hover_data=['Object'],
                               title='Object Size vs Detection Confidence')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Object detection analysis not available.")
    
    with tab3:
        if results.get('caption'):
            st.subheader("💬 AI-Generated Scene Description")
            
            caption = results['caption']
            st.info(f"📝 {caption}")
            
            # Caption analysis
            words = caption.split()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Words", len(words))
            
            with col2:
                avg_word_length = sum(len(word) for word in words) / len(words)
                st.metric("Avg Word Length", f"{avg_word_length:.1f}")
            
            with col3:
                unique_words = len(set(word.lower() for word in words))
                st.metric("Unique Words", unique_words)
            
            # Word frequency analysis
            word_freq = Counter(word.lower().strip('.,!?') for word in words)
            common_words = word_freq.most_common(5)
            
            st.subheader("📊 Word Frequency Analysis")
            if common_words:
                word_df = pd.DataFrame(common_words, columns=['Word', 'Frequency'])
                fig = px.bar(word_df, x='Word', y='Frequency',
                           title='Most Common Words in Description')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Scene description not available.")
    
    with tab4:
        st.subheader("📈 Comprehensive Analytics")
        
        # Model performance comparison
        st.write("**Model Performance Summary:**")
        
        performance_data = []
        
        if results.get('classification'):
            top_class_conf = results['classification'][0]['score']
            performance_data.append({
                'Model': 'Image Classifier',
                'Primary Result': results['classification'][0]['label'],
                'Confidence': top_class_conf,
                'Status': '✅ Success'
            })
        
        if results.get('detection'):
            avg_det_conf = sum(d['score'] for d in results['detection']) / len(results['detection'])
            performance_data.append({
                'Model': 'Object Detector',
                'Primary Result': f"{len(results['detection'])} objects",
                'Confidence': avg_det_conf,
                'Status': '✅ Success'
            })
        
        if results.get('caption'):
            performance_data.append({
                'Model': 'Image Captioner',
                'Primary Result': f"{len(results['caption'].split())} words",
                'Confidence': 0.85,  # Estimated for captioning
                'Status': '✅ Success'
            })
        
        if performance_data:
            perf_df = pd.DataFrame(performance_data)
            st.dataframe(perf_df)
            
            # Model confidence comparison
            fig = px.bar(perf_df, x='Model', y='Confidence',
                        title='Model Confidence Comparison',
                        color='Confidence',
                        color_continuous_scale='viridis')
            st.plotly_chart(fig, use_container_width=True)
        
        # Image properties analysis
        st.subheader("🖼️ Image Properties Analysis")
        
        props = report['image_properties']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Technical Properties:**")
            st.write(f"• **Dimensions:** {props['width']} x {props['height']} pixels")
            st.write(f"• **Aspect Ratio:** {props['aspect_ratio']:.2f}")
            st.write(f"• **Format:** {props['format']}")
            st.write(f"• **Color Mode:** {props['mode']}")
            
            # Megapixels calculation
            megapixels = (props['width'] * props['height']) / 1_000_000
            st.write(f"• **Resolution:** {megapixels:.1f} MP")
        
        with col2:
            st.write("**Analysis Suitability:**")
            
            # Determine image quality for AI analysis
            if props['width'] >= 800 and props['height'] >= 600:
                resolution_quality = "High"
            elif props['width'] >= 400 and props['height'] >= 300:
                resolution_quality = "Medium"
            else:
                resolution_quality = "Low"
            
            st.write(f"• **Resolution Quality:** {resolution_quality}")
            
            if 0.8 <= props['aspect_ratio'] <= 1.25:
                aspect_suitability = "Square (Good for classification)"
            elif props['aspect_ratio'] > 1.25:
                aspect_suitability = "Landscape (Good for detection)"
            else:
                aspect_suitability = "Portrait (Good for objects)"
            
            st.write(f"• **Aspect Suitability:** {aspect_suitability}")
            
            if props['mode'] == 'RGB':
                color_suitability = "Full color (Optimal)"
            elif props['mode'] == 'L':
                color_suitability = "Grayscale (Limited)"
            else:
                color_suitability = f"{props['mode']} (May need conversion)"
            
            st.write(f"• **Color Mode:** {color_suitability}")

# Export functionality
if 'analysis_report' in st.session_state:
    st.markdown("---")
    st.header("📄 Export Analysis Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 Copy Report to Clipboard"):
            report_text = f"""
AI Vision Analysis Report
========================

Image Properties:
- Dimensions: {st.session_state['analysis_report']['image_properties']['width']}x{st.session_state['analysis_report']['image_properties']['height']}
- Format: {st.session_state['analysis_report']['image_properties']['format']}

Analysis Results:
- Primary Classification: {st.session_state['analysis_results'].get('classification', [{}])[0].get('label', 'N/A')}
- Objects Detected: {len(st.session_state['analysis_results'].get('detection', []))}
- Scene Description: {st.session_state['analysis_results'].get('caption', 'N/A')}
            """
            
            st.code(report_text)
            st.success("Report text generated! Copy from the box above.")
    
    with col2:
        # Download report as JSON
        import json
        
        if st.button("💾 Download JSON Report"):
            report_json = json.dumps(st.session_state['analysis_report'], indent=2)
            st.download_button(
                label="📥 Download Report",
                data=report_json,
                file_name="ai_vision_analysis_report.json",
                mime="application/json"
            )

st.write("💡 **Learning Outcome:** Understand multi-modal AI systems, model integration, performance analysis, and comprehensive reporting.")
