# shop-cat

## Project Proposal: shop-cat

### Overview

A collaborative wiki for vehicle repair.<br>
This app allows users to create individual pages for different processes, with step-by-step instructions.<br>
Pages will be linked by keyword and moderated by the community.<br>
The app is meant to be a better-moderated, more structured alternative to traditional vehicle forum writeups and YouTube videos.<br>
It also provides more flexibility and collaborative oversight than a site like Instructables.

### Technologies required (besides typical Hackbright tech stack)

- Wikipedia API: https://www.mediawiki.org/wiki/API:Main_page</li>
- YouTube API: https://developers.google.com/youtube/v3</li>

### Data

**Items and Procedures are the central building blocks of shop-cat.**

A Procedure is tied to a Page with a unique ID, url, etc.  
Procedures consist of Parts, Tools, and Steps.  
A Procedure can require multiple Parts, and Parts can be used in multiple Procedures. (many-many)  
A Procedure can require multiple Tools, and Tools can be used in multiple Procedures. (many-many)  
A Procedure consists of multiple Steps, but a Step can only exist in a specific Procedure. (one-many)  
	***exception/special case: when a Procedure is also a Step (i.e. remove wheels, disconnect battery...)***  
A Part can have multiple Part-Numbers, but a Part-Number can only describe one Part (one-many)  

**Items are things that aren't procedures (e.g. cars or engines).**  
Items consist of Statements.  
An Item is tied to a Page with a unique ID, url, etc.  

Steps also consist of Statements.   
Either an Item or a Step can have many Statements, but a given Statement can only describe one Item or Step. (one-many)

**Statements consist of Properties (e.g. lug nut torque) and References.**   
A Statement can have multiple Properties, but Properties can only describe specific Statements. (one-many)  
A Statement can have multiple References, and References can be used to describe multiple Statements. (many-many)  

*This is the part I am least sure of:*  
Each Property has at least one Value, but can have many Values.   
A Value can represent multiple Properties.  

**Users are connected to the things that they can add, remove, or change in shop-cat.**   
- Only upon creation: Procedures, Items
- Upon editing, adding, or removing: Parts, Part-Nums, Tools, Steps, Statements, Properties, Values, Refs   

Users can edit many things, and each thing can be edited by many different Users. (many-many)      
Therefore, Users are connected to these things via their key in the Contribution-History.


### Roadmap

#### MVP

- User can create a new page to outline a procedure.
- User can add a list of required tools and parts, as well as text-based step-by-step directions.
- User has the option to link to a photo relevant to the procedure.
- Text inputs will feed into a formatted display that can be read easily. 

#### 2.0

- The user will have the option to add or remove steps after the procedure is generated for the first time.
- Allow user to edit existing steps after a procedure is generated.
- User will be able to link to references to specific steps in their procedures.
    - References can link to YouTube videos using the YouTube API.
- User will be able to create general informational pages that are linked to specific cars, not procedures.
- Adapt site to use React (if it doesn't already).

#### 3.0

- Allow user logins.
- Allow users to flag procedures that are unclear.
- All edits made by a certain user (to a procedure or info page) will be tracked in contribution history.
- User can add a central page where all vehicles of a certain make or model are linked.
- Link to the Wikipedia API to get general information about the vehicle on the page.
