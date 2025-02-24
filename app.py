import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd

def extract_data_from_image(image):
    """
    Extracts data from an image (PIL Image object) of Google Ads metrics and returns it as a list of dictionaries.
    """

    try:
        # Use pytesseract to extract text from the image
        text = pytesseract.image_to_string(image)

        # Split the text into lines
        lines = text.splitlines()

        data = []
        i = 0
        while i < len(lines):
            # Try to find metric name, value and change from the text
            if "Cost" in lines[i] or "Conv." in lines[i] or "Rate" in lines[i] or "CTR" in lines[i] or "AVG" in lines[i] or "Search" in lines[i]:
              
              metric_name = lines[i].replace("SEO Works", "").strip() # Extract metric name on the first pass

              # Attempt to reliably extract value by skipping the SEO Works line
              i += 1  # Skip the "SEO Works" line
              if i >= len(lines):
                break

              metric_value = lines[i].strip()
              
              #Check if change is still in bounds
              i += 1
              if i >= len(lines):
                  break
              
              # Extract the change
              metric_change = lines[i].strip()
              
              data.append({
                "Metric": metric_name,
                "Value": metric_value,
                "Change": metric_change
              })
              i += 1 # Advance the iterator to the next metric
            else:
              i += 1 #Advance the iterator
        return data

    except Exception as e:
        st.error(f"Error during OCR or data extraction: {e}")
        return None


def main():
    st.title("Google Ads Metrics Extractor")

    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image.", use_column_width=True)

            extracted_data = extract_data_from_image(image)

            if extracted_data:
                df = pd.DataFrame(extracted_data)
                st.write("### Extracted Data Table")
                st.dataframe(df)  # Use st.dataframe for interactive display

            else:
                st.info("No data extracted from the image.")

        except Exception as e:
            st.error(f"Error processing the image: {e}")


if __name__ == "__main__":
    main()
