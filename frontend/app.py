import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AI Attendance System", layout="wide")

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align: center;'>🎯 AI Face Attendance System</h1>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Navigation", ["📸 Mark Attendance", "📊 View Records"])

# ---------------- MARK ATTENDANCE ----------------
if menu == "📸 Mark Attendance":
    st.subheader("Mark Attendance")

    option = st.radio("Choose Method", ["Upload Image", "Use Camera"])

    img_file = None

    if option == "Upload Image":
        img_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    else:
        img_file = st.camera_input("Take a picture")

    if img_file:
        st.image(img_file, width=300)

        if st.button("✅ Mark Attendance"):
            with st.spinner("Processing..."):
                res = requests.post(
                "https://face-attendance-4-5wml.onrender.com/mark-attendance",
                 files={"file": ("image.jpg", img_file.getvalue(), "image/jpeg")},
                 timeout=30
                 )

            st.write("Status:", res.status_code)
            st.write("Response:", res.text)
            try:
                data = res.json()

                if data["status"] == "success":
                    st.success(f"✅ {data['data']['name']} marked at {data['data']['time']}")
                else:
                    st.error(f"❌ {data['message']}")

            except:
                st.error("⚠️ Server error")

# ---------------- VIEW RECORDS ----------------
elif menu == "📊 View Records":
    st.subheader("Attendance Records")

    res = requests.get("https://face-attendance-4-5wml.onrender.com/attendance")

    try:
        data = res.json()["data"]

        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)

            # Download button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇ Download CSV", csv, "attendance.csv", "text/csv")

        else:
            st.info("No records found")

    except:
        st.error("Error fetching data")
# ---------------- SUMMARY ----------------
   
