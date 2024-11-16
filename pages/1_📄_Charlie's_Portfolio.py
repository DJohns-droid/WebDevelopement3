import streamlit as st
import infoC
import pandas as pd

# About Me
def aboutMeSection():
    st.header("About Me 🧑‍💻")
    st.image(infoC.profile_picture, width=200)
    st.write(infoC.about_me)
    st.write("")
aboutMeSection()

# Sidebar Links
def linksSection():
    st.sidebar.header("Links 🔗")
    st.sidebar.text("Connect with me on LinkedIn")
    linkedin_link = f'<a href="{infoC.my_linkedin_url}"><img src="{infoC.linkedin_image_url}" alt="LinkedIn" width="75" height="75"></a>'
    st.sidebar.markdown(linkedin_link, unsafe_allow_html=True)
    st.sidebar.text("Checkout my work")
    github_link = f'<a href="{infoC.my_github_url}"><img src="{infoC.github_image_url}" alt="Github" width="65" height="65"></a>'
    st.sidebar.markdown(github_link, unsafe_allow_html=True)
    st.sidebar.text("Or email me!")
    email_html = f'<a href="mailto:{infoC.my_email_address}"><img src="{infoC.email_image_url}" alt="Email" width="75" height="75"></a>'
    st.sidebar.markdown(email_html, unsafe_allow_html=True)
linksSection()

# Education
def educationSection(education_data, course_data):
    st.header("Education 🎓")
    st.subheader(f"**{education_data['Institution']}**")
    st.write(f"**Degree:** {education_data['Degree']}")
    st.write(f"**Graduation Date:** {education_data['Graduation Date']}")
    st.write(f"**GPA:** {education_data['GPA']}")
    st.write("**Relevant Coursework:**")
    coursework = pd.DataFrame(course_data)
    st.dataframe(coursework, column_config={
        "code": "Course Code",
        "names": "Course Names",
        "semester_taken": "Semester Taken",
        "skills": "What I Learned"},
        hide_index=True,
    )
    st.write("---")
educationSection(infoC.education_data, infoC.course_data)

# Professional Experience
def experienceSection(experience_data):
    st.header("Professional Experience 💼")
    for job_title, (job_description, image) in experience_data.items():
        expander = st.expander(f"{job_title}")
        expander.image(image, width=250)
        for bullet in job_description:
            expander.write(bullet)
    st.write("---")
experienceSection(infoC.experience_data)

# Projects
def projectSection(projects_data):
    st.header("Projects 🛠")
    for project_name, (project_description, image) in projects_data.items():
        expander = st.expander(f"{project_name}")
        expander.image(image, width=250)
        expander.write(project_description)
    st.write("---")
projectSection(infoC.projects_data)

# Skills
def skillsSection(programming_data, spoken_data):
    st.header("Skills 🧑‍💻")
    st.subheader("Programming Languages")
    for skill, percentage in programming_data.items():
        st.write(f"{skill} {infoC.programming_icons.get(skill, '')}")
        st.progress(percentage)
    st.subheader("Spoken Languages")
    for spoken, proficiency in spoken_data.items():
        st.write(f"{spoken} {infoC.spoken_icons.get(spoken, '')}: {proficiency}")
    st.write("---")
skillsSection(infoC.programming_data, infoC.spoken_data)

# Activities
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
