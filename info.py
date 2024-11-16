
#This File will contain the information to be displayed in your portfolio

#CHANGE BELOW
profile_picture = "Images/profile.jpg"       ##my image here
about_me = ("I'm Daniel Johns, a first-year Electrical Engineering student at Georgia Institute of Technology." +
"I am passionate about leveraging engineering and programming to solve real-world challenges. " +
"With a strong academic foundation and hands-on research experience, I'm excited to grow my expertise in electrical engineering.")


#CHANGE BELOW (OPTIONAL)
linkedin_image_url = "https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg"
github_image_url = "https://cdn-icons-png.flaticon.com/256/25/25231.png"
email_image_url = "https://logowik.com/content/uploads/images/513_email.jpg"

#CHANGE BELOW
my_linkedin_url = "https://www.linkedin.com/in/daniel-johns-a79834257/"
my_github_url = "https://github.com/DJohns-droid"
my_email_address = "daniel.o.johns@gmail.com"


education_data ={
    'Degree': 'Bachelor of Science in Electrical Engineering',
    'Institution': 'Georgia Institute of Technology',
    'Location': 'Atlanta, GA',
    'Graduation Date': 'Expected 2028',
    'GPA': 'N/A'
}
course_data = {
    "code":["CS 1301", "CHEM 1310 ", "MATH 1554", "PSYCH 1101"], 
    "names":["Intro to CS", "Prin of Gen Chem for Engr ", "Linear Algebra", "General Psychology"], 
    "semester_taken":["1st", "1st", "1st", "1st"],
    "skills":["Learned foundational programming concepts and applications", 
              "Developed an understanding of fundamental chemistry principles and their applications in engineering", 
              "Gained proficiency in matrix operations, eigenvalues, and linear transformations",
              "Explored foundational psychological concepts, including memory, learning, and human behavior",],
    }
experience_data = {
    "Research Intern at Crane Nuclear": (
        [
            "- Led research on automating valve testing as part of the Gemini Project",
            "- Investigated the use of strain gauges for electrical current detection in motor-operated valves",
            "- Utilized signal analysis software to record and analyze signals",
            "- Gained hands-on experience with valve mechanics and automation processes",
        ],
        "Images/research.jpg",              ###add image here
    ),
}

projects_data = {
    "Gemini Project - Valve Automation": (
        "Contributed to automating valve testing by researching strain gauge applications, "
        "aiming to improve efficiency and reduce manual testing requirements.",
        "Images/project1.jpg"
    ),
}
programming_data = {
    "Python": 60,
    "Java": 40,
    "HTML": 30,
    "CSS": 30,
    "AutoCAD": 70,
}

#CHANGE BELOW (OPTIONAL)
programming_icons = {
    "Python": "🐍",
    "JavaScript": "🌐",
    "HTML": "📄",
    "CSS": "🎨",
    "AutoCAD": "📐",
}

spoken_icons = {
    "English": "🏳",
    "German": "🏳",
    "Afrikaans": "🏳"
}

#CHANGE BELOW
spoken_data = {
    "English": "Fluent",
    "German": "Intermediate",
    "Afrikaans": "Intermediate",
}
leadership_data = {
    "Mentor at Allatoona Creek Composite": (
        [
            "- Supported junior members of the cycling team with skill-building exercises",
            "- Promoted a culture of teamwork and perseverance within the team",
        ],
        "Images/mentor.png",
    ),

}
activity_data={
    "Varsity Cyclist at Allatoona Creek Composite": (
        [
        "- Competed at varsity level in the Georgia Cycling League",
        "- Mentored junior team members to foster skills and team cohesion",
        "- Achieved 11th place in Varsity at the Georgia State Championships",
        ],
        "Images/cycling.jpg",  # Add the image URL here
    ),
    "Trail Building with SORBA West Georgia": (
        [
            "- Participated in maintaining and building biking trails",
            "- Promoted sustainable trail use within the community",
        ],
        "Images/trail_building.png",  # Add the image URL here
    ),
}
