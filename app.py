import os
import streamlit as st 
from pathlib import Path
import google.generativeai as genai
from PIL import Image
from api_key import api_key

genai.configure(api_key= api_key)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

system_prompt ="""

As a highly skilled medical practitioner specializing in image analysis, you are tasked with examing medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.

Your Responsibilities include:
1. Detailed Analysis: Thoroughly analyze each image , focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomilies or signs of disease. Clearly articulate these findings in a structured form.
3. Recommendations and Next steps: Based on your analysis, suggest potential next steps, inclusing further tests or treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:

1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.'
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions."
4. Your insights are valuable in guiding clinical decisons. Please proceed with the analysis, adhering to the structured approached outlined above.


"""
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)
 # set the page configuration 
st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot:")

#set the logo
st.image("logo.png", width=120)

#set the title
st.markdown(
    "<h1 style='font-size: 40px; text-align: center;'>👩‍⚕️Vital❤️ Image📷 Analytics📊👨‍⚕️</h1>",
    unsafe_allow_html=True
)


#set the subtitle
st.subheader("An application that can help users to identify medical problem using images")
uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png","jpg","jpeg"])

# Process when the file is uploaded
if uploaded_file is not None:
    # Open the image
    image = Image.open(uploaded_file)

    # Resize the image to make it smaller (both length and width)
    small_image = image.resize((300, 300))  # Change (150, 150) as needed

    # Display the resized image
    st.image(small_image, caption="Uploaded Medical Image")
    

submit_button = st.button("Generate the Analysis")


# Process when the button is clicked
if submit_button and uploaded_file is not None:
    try:
         
        # Prepare the prompt with image
        prompt_ports = [
            {"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()},
            system_prompt
        ]

        # Generate response
        response = model.generate_content(prompt_ports)

        # Display the response
        st.subheader("Here is the analysis based on your Image:")
        st.markdown(f"**🔎 AI Findings:**\n\n{response.text}", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")

# Handle case where user clicks the button without an image
elif submit_button and uploaded_file is None:
    st.warning("⚠️ Please upload an image before generating the analysis.")