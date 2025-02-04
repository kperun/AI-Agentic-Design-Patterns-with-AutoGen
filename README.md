# AI Agentic Design Patterns with AutoGen

This course is based on the Coursera course "AI Agentic Design Patterns with AutoGen" [1].

Following libraries are used:
1. pprint: Used to print data in a pretty way.
2. autogen: AutoGen is a framework for creating multi-agent AI applications that can act autonomously or work alongside humans.

All credits to the original creators of this course.

[1] https://www.coursera.org/learn/ai-agentic-design-patterns-with-autogen
[2] https://docs.python.org/3/library/pprint.html
[3] https://github.com/microsoft/autogen


## Sample Conversation with Nested Chat
Critic (to Writer):


        Write a concise but engaging blogpost about
       DeepLearning.AI. Make sure the blogpost is
       within 100 words.
       

--------------------------------------------------------------------------------
Writer (to Critic):

Title: Unveiling the Power of DeepLearning.AI

Step into the world of AI with DeepLearning.AI, a game-changer in the field of artificial intelligence. Offering top-notch courses created by industry experts like Andrew Ng, this platform equips you with the skills to thrive in the age of AI. From computer vision to natural language processing, DeepLearning.AI covers it all. Dive into hands-on projects, gain invaluable insights, and join a community of learners worldwide. Whether you're a beginner or looking to advance your career, DeepLearning.AI caters to all levels of expertise. Elevate your skills, stay ahead of the curve, and unlock endless possibilities with DeepLearning.AI.

--------------------------------------------------------------------------------

********************************************************************************
Starting a new chat....

********************************************************************************
Critic (to Legal Reviewer):

Review the following content. 
            

 Title: Unveiling the Power of DeepLearning.AI

Step into the world of AI with DeepLearning.AI, a game-changer in the field of artificial intelligence. Offering top-notch courses created by industry experts like Andrew Ng, this platform equips you with the skills to thrive in the age of AI. From computer vision to natural language processing, DeepLearning.AI covers it all. Dive into hands-on projects, gain invaluable insights, and join a community of learners worldwide. Whether you're a beginner or looking to advance your career, DeepLearning.AI caters to all levels of expertise. Elevate your skills, stay ahead of the curve, and unlock endless possibilities with DeepLearning.AI.

--------------------------------------------------------------------------------
Legal Reviewer (to Critic):

As a legal reviewer, I would like to provide the following feedback on the content:

- Ensure that any claims made about the effectiveness or outcomes of the courses offered by DeepLearning.AI are substantiated with accurate data or testimonials to avoid any potential misleading advertising issues.
- Verify that the use of phrases like "top-notch" and "game-changer" do not violate any laws related to false advertising, and accurately represent the quality and impact of the courses offered.
- Consider adding a disclaimer regarding the results learners can expect to achieve, to manage expectations and avoid potential liability issues related to promises of career advancement.

--------------------------------------------------------------------------------

********************************************************************************
Starting a new chat....

********************************************************************************
Critic (to SEO Reviewer):

Review the following content. 
            

 Title: Unveiling the Power of DeepLearning.AI

Step into the world of AI with DeepLearning.AI, a game-changer in the field of artificial intelligence. Offering top-notch courses created by industry experts like Andrew Ng, this platform equips you with the skills to thrive in the age of AI. From computer vision to natural language processing, DeepLearning.AI covers it all. Dive into hands-on projects, gain invaluable insights, and join a community of learners worldwide. Whether you're a beginner or looking to advance your career, DeepLearning.AI caters to all levels of expertise. Elevate your skills, stay ahead of the curve, and unlock endless possibilities with DeepLearning.AI.
Context: 
{'Reviewer': 'Legal reviewer', 'Review': 'Ensure that any claims made about the effectiveness or outcomes of the courses offered by DeepLearning.AI are substantiated with accurate data or testimonials to avoid any potential misleading advertising issues. Verify that the use of phrases like "top-notch" and "game-changer" do not violate any laws related to false advertising, and accurately represent the quality and impact of the courses offered. Consider adding a disclaimer regarding the results learners can expect to achieve, to manage expectations and avoid potential liability issues related to promises of career advancement.'}

--------------------------------------------------------------------------------
SEO Reviewer (to Critic):

As an SEO reviewer: 

- Include specific data or testimonials to support claims about the effectiveness of courses on DeepLearning.AI
- Avoid using exaggerated phrases like "top-notch" and "game-changer" to ensure compliance with advertising laws
- Consider adding a disclaimer to manage expectations about career advancements to mitigate potential liability issues

--------------------------------------------------------------------------------

********************************************************************************
Starting a new chat....

********************************************************************************
Critic (to Ethics Reviewer):

Review the following content. 
            

 Title: Unveiling the Power of DeepLearning.AI

Step into the world of AI with DeepLearning.AI, a game-changer in the field of artificial intelligence. Offering top-notch courses created by industry experts like Andrew Ng, this platform equips you with the skills to thrive in the age of AI. From computer vision to natural language processing, DeepLearning.AI covers it all. Dive into hands-on projects, gain invaluable insights, and join a community of learners worldwide. Whether you're a beginner or looking to advance your career, DeepLearning.AI caters to all levels of expertise. Elevate your skills, stay ahead of the curve, and unlock endless possibilities with DeepLearning.AI.
Context: 
{'Reviewer': 'Legal reviewer', 'Review': 'Ensure that any claims made about the effectiveness or outcomes of the courses offered by DeepLearning.AI are substantiated with accurate data or testimonials to avoid any potential misleading advertising issues. Verify that the use of phrases like "top-notch" and "game-changer" do not violate any laws related to false advertising, and accurately represent the quality and impact of the courses offered. Consider adding a disclaimer regarding the results learners can expect to achieve, to manage expectations and avoid potential liability issues related to promises of career advancement.'}
{"Reviewer": "SEO reviewer", "Review": "- Include specific data or testimonials to support claims about the effectiveness of courses on DeepLearning.AI\n- Avoid using exaggerated phrases like 'top-notch' and 'game-changer' to ensure compliance with advertising laws\n- Consider adding a disclaimer to manage expectations about career advancements to mitigate potential liability issues"}

--------------------------------------------------------------------------------
Ethics Reviewer (to Critic):

As an ethics reviewer: 

1. Ensure that any claims made about the effectiveness or outcomes of the courses offered by DeepLearning.AI are substantiated with accurate data or testimonials to avoid misleading advertising. 
2. Avoid using exaggerated phrases like "top-notch" and "game-changer" in the promotion to ensure compliance with advertising laws. 
3. Consider adding a disclaimer to manage expectations about career advancements to mitigate potential liability issues.

--------------------------------------------------------------------------------

********************************************************************************
Starting a new chat....

********************************************************************************
Critic (to Meta Reviewer):

Aggregate feedback from all reviewers and give final suggestions on the writing.
Context: 
{'Reviewer': 'Legal reviewer', 'Review': 'Ensure that any claims made about the effectiveness or outcomes of the courses offered by DeepLearning.AI are substantiated with accurate data or testimonials to avoid any potential misleading advertising issues. Verify that the use of phrases like "top-notch" and "game-changer" do not violate any laws related to false advertising, and accurately represent the quality and impact of the courses offered. Consider adding a disclaimer regarding the results learners can expect to achieve, to manage expectations and avoid potential liability issues related to promises of career advancement.'}
{"Reviewer": "SEO reviewer", "Review": "- Include specific data or testimonials to support claims about the effectiveness of courses on DeepLearning.AI\n- Avoid using exaggerated phrases like 'top-notch' and 'game-changer' to ensure compliance with advertising laws\n- Consider adding a disclaimer to manage expectations about career advancements to mitigate potential liability issues"}
{'Reviewer': 'Ethics reviewer', 'Review': 'Ensure that all claims are substantiated with accurate data or testimonials. Avoid using exaggerated phrases in promotions and consider adding a disclaimer about career advancements.'}

--------------------------------------------------------------------------------
Meta Reviewer (to Critic):

The aggregate feedback from all reviewers highlights the importance of substantiating claims with accurate data or testimonials regarding the effectiveness of DeepLearning.AI courses. Additionally, it is crucial to avoid exaggerated phrases such as "top-notch" and "game-changer" to comply with advertising laws and ethical standards. Adding a disclaimer about the results learners can expect in terms of career advancements is also recommended to manage expectations and mitigate potential liability issues.

In conclusion, it is essential to back up all claims with evidence, use language that accurately represents the quality of the courses, and provide transparent information to learners about the potential outcomes they can achieve. By addressing these suggestions, the content can uphold ethical standards, comply with legal requirements, and provide a clear understanding to the audience.

--------------------------------------------------------------------------------
Critic (to Writer):

The aggregate feedback from all reviewers highlights the importance of substantiating claims with accurate data or testimonials regarding the effectiveness of DeepLearning.AI courses. Additionally, it is crucial to avoid exaggerated phrases such as "top-notch" and "game-changer" to comply with advertising laws and ethical standards. Adding a disclaimer about the results learners can expect in terms of career advancements is also recommended to manage expectations and mitigate potential liability issues.

In conclusion, it is essential to back up all claims with evidence, use language that accurately represents the quality of the courses, and provide transparent information to learners about the potential outcomes they can achieve. By addressing these suggestions, the content can uphold ethical standards, comply with legal requirements, and provide a clear understanding to the audience.

--------------------------------------------------------------------------------
Writer (to Critic):

Title: Unveiling the Potential of DeepLearning.AI

Embark on your AI journey with DeepLearning.AI, a leading platform that offers expertly crafted courses by renowned professionals like Andrew Ng. Covering diverse topics from computer vision to natural language processing, this resource provides a comprehensive learning experience. Engage in practical projects, gain industry insights, and connect with a global community of learners. Whether you're a novice or aiming for career growth, DeepLearning.AI caters to all skill levels. Develop your expertise, keep pace with industry trends, and explore new opportunities with DeepLearning.AI. Note: Individual outcomes may vary; please manage expectations accordingly.

--------------------------------------------------------------------------------