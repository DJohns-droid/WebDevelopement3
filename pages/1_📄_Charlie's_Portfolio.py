import streamlit as st
import infoC
import pandas as pd

# Set page configuration (optional)
st.set_page_config(page_title="Charlie's Portfolio", page_icon=":briefcase:", layout="wide")

# About Me Section
def aboutMeSection():
    st.header("About Me 🧑‍💻")
    st.image(infoC.profile_picture, width=200)
    st.write(infoC.about_me)
    st.write("")

aboutMeSection()

# Sidebar Links Section
def linksSection():
    st.sidebar.header("Links 🔗")
    
    # LinkedIn
    st.sidebar.subheader("Connect with me on LinkedIn")
    linkedin_link = f'<a href="{infoC.my_linkedin_url}" target="_blank"><img src="{infoC.linkedin_image_url}" alt="LinkedIn" width="75" height="75"></a>'
    st.sidebar.markdown(linkedin_link, unsafe_allow_html=True)
    
    # GitHub
    st.sidebar.subheader("Checkout my GitHub")
    github_link = f'<a href="{infoC.my_github_url}" target="_blank"><img src="{infoC.github_image_url}" alt="GitHub" width="65" height="65"></a>'
    st.sidebar.markdown(github_link, unsafe_allow_html=True)
    
    # Email
    st.sidebar.subheader("Or Email me!")
    email_html = f'<a href="mailto:{infoC.my_email_address}"><img src="{infoC.email_image_url}" alt="Email" width="75" height="75"></a>'
    st.sidebar.markdown(email_html, unsafe_allow_html=True)

linksSection()

# Education Section
def educationSection(education_data, course_data):
    st.header("Education 🎓")
    st.subheader(f"**{education_data['Institution']}**")
    st.write(f"**Degree:** {education_data['Degree']}")
    st.write(f"**Graduation Date:** {education_data['Graduation Date']}")
    st.write(f"**GPA:** {education_data['GPA']}")
    st.write("**Relevant Coursework:**")
    
    # Create DataFrame for coursework
    coursework = pd.DataFrame(course_data)
    
    # Display DataFrame with custom column names
    st.dataframe(
        coursework.rename(columns={
            "code": "Course Code",
            "names": "Course Names",
            "semester_taken": "Semester Taken",
            "skills": "What I Learned"
        }),
        hide_index=True,
    )
    st.write("---")

educationSection(infoC.education_data, infoC.course_data)

# Professional Experience Section
def experienceSection(experience_data):
    st.header("Professional Experience 💼")
    for job_title, (job_description, image) in experience_data.items():
        expander = st.expander(f"{job_title}")
        expander.image(image, width=250)
        for bullet in job_description:
            expander.write(bullet)
    st.write("---")

experienceSection(infoC.experience_data)

# Projects Section
def projectSection(projects_data):
    st.header("Projects 🛠")
    for project_name, (project_description, image) in projects_data.items():
        expander = st.expander(f"{project_name}")
        expander.image(image, width=250)
        expander.write(project_description)
    st.write("---")

projectSection(infoC.projects_data)

# Skills Section
def skillsSection(programming_data, spoken_data):
    st.header("Skills 🧑‍💻")
    
    # Programming Languages
    st.subheader("Programming Languages")
    for skill, percentage in programming_data.items():
        icon = infoC.programming_icons.get(skill, '')
        st.write(f"{skill} {icon}")
        st.progress(percentage)
    
    st.write("")  # Add some space
    
    # Spoken Languages
    st.subheader("Spoken Languages")
    for spoken, proficiency in spoken_data.items():
        icon = infoC.spoken_icons.get(spoken, '')
        st.write(f"{spoken} {icon}: {proficiency}")
    
    st.write("---")

skillsSection(infoC.programming_data, infoC.spoken_data)

# Activities Section
def activitiesSection(leadership_data, activity_data):
    st.header("Activities 🌟")
    tab1, tab2 = st.tabs(["Leadership", "Community Service"])
    
    with tab1:
        st.subheader("Leadership")
        for title, (details, image) in leadership_data.items():
            expander = st.expander(f"{title}")
            expander.image(image, width=250)
            for bullet in details:
                expander.write(bullet)
    
    with tab2:
        st.subheader("Community Service")
        for title, (details, image) in activity_data.items():
            expander = st.expander(f"{title}")
            expander.image(image, width=250)
            for bullet in details:
                expander.write(bullet)
    
    st.write("---")

activitiesSection(infoC.leadership_data, infoC.activity_data)
