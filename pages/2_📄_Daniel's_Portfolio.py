import streamlit as st
import info
import pandas as pd

##abt me
def about_me_section():
    st.header("About Me (Outdated Portfolio, please ignore)")
    st.image(info.profile_picture, width = 200)
    st.write(info.about_me)
    st.write("---")
about_me_section()

#Sidebar links
def links_section():
    st.sidebar.header("Links 🔗")
    st.sidebar.text("Connect with me on LinkedIn")
    linkedin_link = f'<a href="{info.my_linkedin_url}"><img src="{info.linkedin_image_url}" alt="linkedin_link" width="75" height="75"></a>'
    st.sidebar.markdown(linkedin_link, unsafe_allow_html=True)
    st.sidebar.text("Checkout my work")
    github_link=f'<a href="{info.my_github_url}"><img src="{info.github_image_url}" alt="Github" width="65" height="65"></a>'
    st.sidebar.markdown(github_link, unsafe_allow_html=True)
    st.sidebar.text("Or email me!")
    email_html=f'<a href="{info.my_email_address}"><img src="{info.email_image_url}" alt="Email" width="75" height="75"></a>'
    st.sidebar.markdown(email_html, unsafe_allow_html=True)
links_section()

#Education
def education_section(education_data, course_data):
    st.header("Education 🎓")
    st.markdown(f"### **{education_data['Institution']}**")
    st.markdown(f"**Degree:** {education_data['Degree']}")
    st.markdown(f"**Graduation Date:** {education_data['Graduation Date']}")
    st.markdown(f"**GPA:** {education_data['GPA']}")
    st.markdown("**Relevant Coursework:**")
    coursework = pd.DataFrame(course_data)
    st.dataframe(coursework, column_config={
        "code":"Course Code",
        "names":"Course Name",
        "semester_taken":"Semester Taken",
        "skills":"What I learned"},
        hide_index=True,
    )
    st.write("---")
education_section(info.education_data, info.course_data)

#Professional Experience
def experience_section(experience_data):
    st.header("Professional Experience 💼")
    for job_title, (job_description, image) in experience_data.items():
        expander = st.expander(f"{job_title}")
        expander.image(image, width = 250)
        for bullet in job_description:
            expander.write(bullet)
    st.write("---")
experience_section(info.experience_data)

#Projects
def project_section(projects_data):
    st.header("Projects 🛠")
    for project_name, (project_description, image) in projects_data.items():  # Unpack description and image
        expander = st.expander(f"{project_name}")                   ##updated project section
        expander.write(project_description)
        if image:  # Check if the image path exists
            expander.image(image, caption=project_name, width=250)  # Render the image
    st.write("---")
project_section(info.projects_data)

#Skills
def skills_section(programming_data, spoken_data):
    st.header("Skills 🧑‍💻")
    st.subheader("Programming Languages")
    for skill,percentage in programming_data.items():
        st.write(f"{skill}{info.programming_icons.get(skill, '')}")
        st.progress(percentage)
    st.subheader("Spoken Languages")
    for spoken, proficiency in spoken_data.items():
        st.write(f"{spoken}{info.spoken_icons.get(spoken, '')}:{proficiency}")

    st.write("---")
skills_section(info.programming_data, info.spoken_data)

#Activities
def activities_section(leadership_data, activity_data):
    st.header("Activities 🌟")
    tab1, tab2 = st.tabs(["Leadership", "Community Service"])
    
    # Leadership Tab
    with tab1:
        st.subheader("Leadership")
        for title, (details, image) in leadership_data.items():
            expander = st.expander(f"{title}")
            if image:  # Check if image exists
                expander.image(image, width=250)
            for bullet in details:
                expander.write(bullet)
    
    # Community Service Tab
    with tab2:
        st.subheader("Community Service")
        for title, (details, image) in activity_data.items():  # Unpack details and image
            expander = st.expander(f"{title}")
            if image:  # Check if image exists                          
                expander.image(image, width=250)
            for bullet in details:
                expander.write(bullet)
    st.write("---")     
activities_section(info.leadership_data, info.activity_data)
