# SOFTWARE ENGINEERING PROJECT DOCUMENTATION TEMPLATE

## RATIONALE

This documentation template is designed to help you complete **Component A - Project Documentation** of your Software Engineering Year 12 Personal Project.

**The template supports the four required stages from the syllabus:**

- Identifying and Defining
- Research and Planning
- Producing and Implementing
- Testing and Evaluating

**It also includes essential modelling tools (which are EXAMINABLE in the HSC!):**

- Context Diagram
- Data Flow Diagrams (DFDs)
- Structure Chart
- IPO Chart
- Data Dictionary
- UML Class Diagram (if OOP)

## TITLE PAGE

**Project Title: Button Simulator: Excavation Discoveries, but bad**  
**Student Name: Anthony Revel**  
**Date: 2/03/2026**  
**Course:** Software Engineering Stage 6  
**GitHub URL (if applicable):**

Table of Contents

[SOFTWARE ENGINEERING PROJECT DOCUMENTATION TEMPLATE 1](#software-engineering-project-documentation-template)

[RATIONALE 1](#rationale)

[TITLE PAGE 2](#title-page)

[Syllabus Requirements 5](#syllabus-requirements)

[1\. Identifying and Defining 7](#1-identifying-and-defining)

[1.1 Problem Statement 7](#11-problem-statement)

[1.2 Project Purpose and Boundaries 7](#12-project-purpose-and-boundaries)

[1.3 Stakeholder Requirements 7](#13-stakeholder-requirements)

[1.4 Functional Requirements 7](#14-functional-requirements)

[1.5 Non-Functional Requirements 7](#15-non-functional-requirements)

[1.6 Constraints 7](#16-constraints)

[1.7 Requirements Analysis and Prioritisation 8](#17-requirements-analysis-and-prioritisation)

[2\. Research and Planning 9](#2-research-and-planning)

[2.1 Development Methodology 9](#21-development-methodology)

[2.2 Tools and Technologies 9](#22-tools-and-technologies)

[2.3 Gantt Chart / Timeline 9](#23-gantt-chart--timeline)

[2.4 Communication Plan 9](#24-communication-plan)

[2.5 Resource Allocation Justification 9](#25-resource-allocation-justification)

[3\. System Design 10](#3-system-design)

[3.1 Context Diagram 10](#31-context-diagram)

[3.2 Data Flow Diagrams (Level 0 and Level 1) 10](#32-data-flow-diagrams-level-0-and-level-1)

[3.3 Structure Chart 10](#33-structure-chart)

[3.4 IPO Chart 10](#34-ipo-chart)

[3.5 Data Dictionary 10](#35-data-dictionary)

[3.6 UML Class Diagram (if OOP) 10](#36-uml-class-diagram-if-oop)

[4\. Producing and Implementing 11](#4-producing-and-implementing)

[4.1 Development Process 11](#41-development-process)

[4.2 Key Features Developed 11](#42-key-features-developed)

[4.2.1 Back-End Engineering Contribution 11](#421-back-end-engineering-contribution)

[4.3 Screenshots of Interface 11](#43-screenshots-of-interface)

[4.4 Version Control Summary (Optional) 11](#44-version-control-summary-optional)

[5\. Testing and Evaluation 12](#5-testing-and-evaluation)

[5.1 Testing Methods Used 12](#51-testing-methods-used)

[5.2 Test Cases and Results 12](#52-test-cases-and-results)

[5.3 Evaluation Against Requirements 12](#53-evaluation-against-requirements)

[5.4 Improvements and Future Development 12](#54-improvements-and-future-development)

[6\. Feedback, Security and Reflection 13](#6-feedback-security-and-reflection)

[6.1 Summary of Client or Peer Feedback 13](#61-summary-of-client-or-peer-feedback)

[6.2 Secure Software Design and Data Handling 13](#62-secure-software-design-and-data-handling)

[6.3 Personal Reflection 13](#63-personal-reflection)

[7\. Appendices 14](#7-appendices)

## Syllabus Requirements

| **Syllabus Requirement** | **Template Section** | **STATUS** |
| --- | --- | --- |
| Identifying problem, feasibility, and requirements | Section 1.1 - 1.6 |<b><span style="background: linear-gradient(90deg, #ffff00, #ffff66, #ffff00); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">In Progress</span></b>|
| Stakeholder and client expectations and feedback | Section 1.3, Section 6.1 |<b><span style="background: linear-gradient(90deg, #ffff00, #ffff66, #ffff00); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">In Progress</span></b>|
| Functional and non-functional requirements | Section 1.4, 1.5 |<b><span style="background: linear-gradient(90deg, #00ff00, #88ff88, #00ff00); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">Complete</span></b>|
| Project constraints | Section 1.6 |<b><span style="background: linear-gradient(90deg, #00ff00, #88ff88, #00ff00); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">Complete</span></b>|
| Planning methodology and Gantt chart | Section 2.1 - 2.3 |<b><span style="background: linear-gradient(90deg, #ff0000, #aa0000, #ff0000); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">Incomplete</span>|
| Tools and language justification | Section 2.2 |<b><span style="background: linear-gradient(90deg, #ff0000, #aa0000, #ff0000); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">Incomplete</span>|
| Communication with clients and feedback loops | Section 2.4, 6.1 |<b><span style="background: linear-gradient(90deg, #ff0000, #aa0000, #ff0000); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">Incomplete</span>|
| Context Diagram and DFDs | Section 3.1, 3.2 |<b><span style="background: linear-gradient(90deg, #ff0000, #aa0000, #ff0000); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">Incomplete</span>|
| Structure Chart and IPO | Section 3.3, 3.4 |<b><span style="background: linear-gradient(90deg, #ff0000, #aa0000, #ff0000); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">Incomplete</span>|
| Data Dictionary | Section 3.5 |<b><span style="background: linear-gradient(90deg, #ff0000, #aa0000, #ff0000); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">Incomplete</span>|
| UML Class Diagram (if applicable) | Section 3.6 |<b><span style="background: linear-gradient(90deg, #ff0000, #aa0000, #ff0000); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">Incomplete</span>|
| Code implementation and key features | Section 4.1 - 4.2 |<b><span style="background: linear-gradient(90deg, #ff0000, #aa0000, #ff0000); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">Incomplete</span>|
| UI screenshots and explanation | Section 4.3 |<b><span style="background: linear-gradient(90deg, #ff0000, #aa0000, #ff0000); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">Incomplete</span>|
| Version control and iterations (optional) | Section 4.4 |<b><span style="background: linear-gradient(90deg, #ff0000, #aa0000, #ff0000); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">Incomplete</span>|
| Testing methods and test cases | Section 5.1 - 5.2 |<b><span style="background: linear-gradient(90deg, #ff0000, #aa0000, #ff0000); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">Incomplete</span>|
| Evaluation of requirements and software effectiveness | Section 5.3 |<b><span style="background: linear-gradient(90deg, #ff0000, #aa0000, #ff0000); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">Incomplete</span>|
| Suggestions for improvement and future development | Section 6.1 - 6.3 |<b><span style="background: linear-gradient(90deg, #ff0000, #aa0000, #ff0000); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">Incomplete</span>|
| Analyse and respond to feedback,<br><br>evaluate the effectiveness of a software solution | Section 6.2 |<b><span style="background: linear-gradient(90deg, #ff0000, #aa0000, #ff0000); -webkit-background-clip: text;-webkit-text-fill-color: transparent;">Incomplete</span>|

# 1\. Identifying and Defining
## 1.1 Problem Statement



**Outline** the problem or opportunity that the project addresses. Consider who is affected by this issue.

**Explain** why this problem or opportunity is significant.

**Justify** the development of a software solution as an appropriate response.

## 1.2 Project Purpose and Boundaries

This project is an attempt to create a faithful recreation of the now deprecated Roblox game [Button Simulator: Excavation Discoveries](https://example.com) in a **GUI** format, recreating the main mechanics of the game and some of its various puzzles with some creative liberties.

## 1.3 Stakeholder Requirements

**Identify** stakeholders (client, users, teacher, peers).

**Describe** their needs, expectations, and how these influenced the project direction.

## 1.4 Functional Requirements

- The system must be capable of faithfully recreating the entire main progression from Button Simulator: Excavation Discoveries
- The system must be capable of handling overly large numbers that may surpass the inherent float infinity without issue
- The system must be capable of recreating a vast majority of mechanics from Button Simulator: Excavation Discoveries (although creative liberties may be taken), including but not limited to:
  - Geode buttons
  - Recovery buttons
  - Worlds (Areas with their own progression that may or may not affect the main progression)
  - Subworlds (Worlds that act as bonus challenges rather than standalone progressions, typically inherent a portion of the main progression)
  - Crafting
  - Secret/Exclusive stats (Highly puzzle-based/skill-based stats which can be earnt through alternative means that do not necessarily relate to the main progression, puzzles may expand beyond the direct scope of the system and onto the internet)
  - Cost buttons (buttons which only take a set amount to give a currency)
  - Reset buttons (buttons which reset all stats below a certain stat to give an amount of that stat)
  - Gamepasses (linked to the original game to support the developers)
- The system must be capable of retaining user progress between sessions

## 1.5 Non-Functional Requirements

- The system must be able to load content in under 1 second (excluding the initial boot time)
- The system should be easily usable with clear tutorials for the system's basic mechanics
- The system must be capable of safely handling sensitive user data such as account passwords
- The system should be consistently usable with minimal downtime with proper checks to prevent potential DDOS attacks and similar vulnerabilities.

## 1.6 Constraints

- The project must be completed by Term 2 Week 11
- It is not feasible to create the Roblox physics engine in any regard, nor is it feasible to create the project in Luau with Roblox Studio as it would also infringe upon the copyright that exists for the game on Roblox

## 1.7 Requirements Analysis and Prioritisation

**Analyse** the functional and non-functional requirements. In your analysis, consider:

- which requirements were prioritised and why,
- trade-offs made due to constraints,
- how requirements align with the identified problem or opportunity

# 2\. Research and Planning

## 2.1 Development Methodology

**Describe** the development approach used (e.g. Agile, Waterfall, WAgile).

**Justify** the suitability of this methodology. You could consider…

- Project size and complexity
- Time constraints
- Feedback and iteration requirements

## 2.2 Tools and Technologies

**Justify** the selection of software applications, engines, developer tools, programming languages, IDEs, frameworks, libraries and/or hardware components.

**Explain** how these tools supported efficient and effective development.

## 2.3 Gantt Chart / Timeline

Include a timeline showing key project milestones.

**Explain** how time was allocated to planning, development, testing, and evaluation.

## 2.4 Communication Plan

**Explain** how client or peer feedback was obtained and incorporated.

## 2.5 Resource Allocation Justification

**Justify** the resource allocation for the project, including:

- Time
- Software and hardware tools
- Human input (client, peers, teacher feedback)

# 3\. System Design

This section justifies the use of modelling tools to represent system structure, data flow, and processing logic prior to implementation.

## 3.1 Context Diagram

Include a context diagram showing system boundaries and external entities.

## 3.2 Data Flow Diagrams (Level 0 and Level 1)

Illustrate how data moves through the system.

## 3.3 Structure Chart

Show the modular structure of the system and relationships between modules.

## 3.4 IPO Chart

| Input | Process | Output |
| --- | --- | --- |
|     |     |     |

## 3.5 Data Dictionary

| Name | Type | Description |
| --- | --- | --- |
| username | String | Stores user login name |
| taskList | List | Stores user tasks |
| sessionData | JSON | Stores session state |

## 3.6 UML Class Diagram (if OOP)

Include a class diagram if your project uses an OOP approach.

**Explain** the class structure and relationships.

# 4\. Producing and Implementing

## 4.1 Development Process

**Describe** how the solution was built and implemented.

**Justify** the engineering techniques used, such as:

- Modular design
- Object-oriented principles
- Reuse of code
- Validation and error handling

## 4.2 Key Features Developed

**Describe** the core features of the system.

**Justify** their inclusion.

## 4.2.1 Back-End Engineering Contribution

**Explain** how back-end engineering contributed to the success and ease of use of the software, including

- Data processing
- Validation and logic
- Storage and retrieval
- Authentication (if applicable)

## 4.3 Screenshots of Interface

Include annotated screenshots explaining how the user interacts with the system.

## 4.4 Version Control Summary (Optional)

**Summarise** commits, iterations, or sprints if version control was used.

# 5\. Testing and Evaluation

## 5.1 Testing Methods Used

Describe testing approaches, such as:

- Unit testing
- Integration testing
- User testing

**Explain** how testing results were used to improve performance, efficiency, or reliability.

## 5.2 Test Cases and Results

| Test ID | Description | Expected Result | Actual Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| TC01 | Valid login | Success message | Success message | Pass |
| TC02 | Invalid login | Error message | Error message | Pass |

## 5.3 Evaluation Against Requirements

**Evaluate** how effectively the solution meets the identified functional and non-functional requirements. Consider your ongoing quality assurance processes.

**Evaluate** your project in terms of how effectively you addressed compliance and legislative requirements (consider privacy, use of data, etc).

## 5.4 Improvements and Future Development

**Outline** your project's limitations.

**Explain** realistic future enhancements.

## 5.5 Evaluation of Social, Ethical and Communication Issues

**Evaluate** your project in terms of

# 6\. Feedback, Security and Reflection

## 6.1 Summary of Client or Peer Feedback

**Summarise** feedback received and explain how it influenced development.

You could collect a **'PMI' (Plus, Minus, Implication)** table from **at least three** different people after testing, or **record and summarise an interview** with **at least three** three people who test the software.

**Evaluate** your use of feedback to improve your project:

- Consider your individual workflow and how well you responded to peer / stakeholder feedback
- Consider how well you involved, empowered or negotiated with a peer/client throughout the process.

## 6.2 Secure Software Design and Data Handling

**Evaluate** the approach undertaken to safely and securely collect, use, and store data.

Your evaluation should address:

- Secure coding practices applied during development
- Input validation and error handling
- Data storage and protection methods
- The impact of secure software design on user trust, data integrity, and system reliability

## 6.3 Personal Reflection

**Reflect** on what you learned during the project, including

- Software engineering skills developed
- Challenges encountered and how they were overcome

# 7\. Appendices

- Full Gantt Chart
- Complete Data Dictionary
- Full Test Logs
- Raw Feedback Notes
- Exemplar Code Snippets