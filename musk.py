import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import networkx as nx
import numpy as np
from PIL import Image
import os

# Use Orbitron font
orbitron_font_path = "Orbitron-Regular.ttf"  # Adjust if necessary
orbitron_font = fm.FontProperties(fname=orbitron_font_path) if os.path.exists(orbitron_font_path) else fm.FontProperties()

# Define abbreviations for government agencies
agency_abbreviations = {
    "Department of Labor (DOL)": "DOL",
    "Consumer Financial Protection Bureau (CFPB)": "CFPB",
    "U.S. Agency for International Development (USAID)": "USAID",
    "Department of Transportation (DOT)": "DOT",
    "U.S. Department of Agriculture (USDA)": "USDA",
    "Environmental Protection Agency (EPA)": "EPA",
    "Federal Election Commission (FEC)": "FEC",
    "Department of the Interior (DOI)": "DOI",
    "Department of Defense (DOD)": "DOD",
    "Department of Justice (DOJ)": "DOJ",
    "Securities and Exchange Commission (SEC)": "SEC",
    "Office of Government Ethics (OGE)": "OGE"
}

# Define government agencies and Musk-led companies with correct image paths
agency_logos = {
    "Department of Labor (DOL)": "Seal_of_the_United_States_Department_of_Labor.jpeg",
    "Consumer Financial Protection Bureau (CFPB)": "Seal_of_the_Consumer_Financial_Protection_Bureau.jpeg",
    "U.S. Agency for International Development (USAID)": "Seal_of_the_United_States_Agency_for_International_Development.jpeg",
    "Department of Transportation (DOT)": "United_States_Department_of_Transportation_seal.jpeg",
    "U.S. Department of Agriculture (USDA)": "Logo_of_the_United_States_Department_of_Agriculture.jpeg",
    "Environmental Protection Agency (EPA)": "Seal_of_the_United_States_Environmental_Protection_Agency.jpeg",
    "Federal Election Commission (FEC)": "Seal_of_the_United_States_Federal_Election_Commission.jpeg",
    "Department of the Interior (DOI)": "Seal_of_the_United_States_Department_of_the_Interior.jpeg",
    "Department of Defense (DOD)": "Seal_of_the_United_States_Department_of_Defense.jpeg",
    "Department of Justice (DOJ)": "Seal_of_the_United_States_Department_of_Justice.jpeg",
    "Securities and Exchange Commission (SEC)": "Seal_of_the_United_States_Securities_and_Exchange_Commission.jpeg",
    "Office of Government Ethics (OGE)": "Seal_of_the_United_States_Office_Of_Government_Ethics.jpeg"
}

# Musk-led companies
company_logos = {
    "Tesla": "Tesla_logo.jpeg",
    "SpaceX": "SpaceX_logo_black.jpeg",
    "X (formerly Twitter)": "X_logo.jpeg",
    "Neuralink": "Neuralink_logo.jpeg",
    "Starlink": "Starlink_Logo.jpeg"
}

# Define the connections (who is investigating whom)
connections = {
    "Department of Labor (DOL)": ["Tesla", "SpaceX"],
    "Consumer Financial Protection Bureau (CFPB)": ["Tesla"],
    "U.S. Agency for International Development (USAID)": ["Starlink"],
    "Department of Transportation (DOT)": ["Tesla", "SpaceX"],
    "U.S. Department of Agriculture (USDA)": ["Neuralink"],
    "Environmental Protection Agency (EPA)": ["Tesla"],
    "Federal Election Commission (FEC)": ["X (formerly Twitter)"],
    "Department of the Interior (DOI)": ["SpaceX"],
    "Department of Defense (DOD)": ["SpaceX"],
    "Department of Justice (DOJ)": ["SpaceX", "Tesla"],
    "Securities and Exchange Commission (SEC)": ["X (formerly Twitter)"],
    "Office of Government Ethics (OGE)": ["X (formerly Twitter)"]
}

# Count the number of investigations per Musk-led company
company_investigation_counts = {company: 0 for company in company_logos.keys()}
for agencies in connections.values():
    for company in agencies:
        company_investigation_counts[company] += 1

# Sort companies by the number of investigations (descending)
sorted_companies = sorted(company_investigation_counts.keys(), key=lambda c: -company_investigation_counts[c])
reversed_companies = list(reversed(sorted_companies))

# Positioning nodes manually for better alignment
pos = {}
x_left, x_right = -1, 1  
y_spacing = 2.0  

# Assign positions for government agencies
for i, agency in enumerate(agency_logos.keys()):
    pos[agency] = (x_left, -i * y_spacing)

# Assign positions for Musk-led companies (sorted order)
company_y_positions = np.linspace(-len(agency_logos) * y_spacing + y_spacing, 0, len(company_logos))
for i, (company, y_pos) in enumerate(zip(reversed_companies, company_y_positions)):
    pos[company] = (x_right, y_pos)

# Define a cool winter-themed color palette because I love looking good. 
winter_colors = [
    "#1E90FF", "#4682B4", "#5F9EA0", "#00CED1", "#20B2AA", "#708090",
    "#778899", "#87CEEB", "#B0C4DE", "#2F4F4F", "#6495ED", "#00BFFF"
]

shifted_companies_20px = {"SpaceX", "X (formerly Twitter)", "Starlink"}
shifted_companies_10px = {"Neuralink"}

# Dictionary to track vertical spacing adjustments for each company
company_y_offsets = {company: 0 for company in reversed_companies}

# Create figure
fig, ax = plt.subplots(figsize=(14, 14), facecolor="white") 

# Draw connections
for idx, agency in enumerate(agency_logos.keys()):
    if agency in connections:
        agency_x, agency_y = pos[agency]
        agency_x_right = agency_x + 0.1  

        for company in sorted_companies:  
            if company in connections[agency]:
                company_x, company_y = pos[company]

                if company in shifted_companies_20px:
                    company_x_left = company_x - 0.2  
                elif company in shifted_companies_10px:
                    company_x_left = company_x - 0.15  
                else:
                    company_x_left = company_x - 0.1  

                mid_x = (agency_x_right + company_x_left) / 2
                mid_y = company_y - company_y_offsets[company]  

                company_y_offsets[company] += 0.3  

                curve_x = [agency_x_right, mid_x, company_x_left]
                curve_y = [agency_y, mid_y, company_y]

                ax.plot(curve_x, curve_y, color=winter_colors[idx % len(winter_colors)], linestyle="-", linewidth=2, alpha=0.9)

# Function to add images
def add_images(image_dict, positions, ax, width=0.15, height_multiplier=1.0):
    for name, filepath in image_dict.items():
        if os.path.exists(filepath):
            img = Image.open(filepath)
            img = img.resize((150, int(225 * height_multiplier)))  
            img_extent = (positions[name][0] - width, positions[name][0] + width,
                          positions[name][1] - (0.3 * height_multiplier), positions[name][1] + (0.3 * height_multiplier))
            ax.imshow(img, extent=img_extent, aspect='auto')

add_images(agency_logos, pos, ax, width=0.075, height_multiplier=2.5)  # Make agency lgoos 2.5x taller.
add_images(company_logos, pos, ax, width=0.15, height_multiplier=3.0)  # Make Musk-led logos 3x taller

# Add investigation count underneath Musk-led companies. Make sure to use the font we defined earlier. 
for company in reversed_companies:
    num_investigations = company_investigation_counts[company]
    investigation_text = f"{num_investigations} agency" if num_investigations == 1 else f"{num_investigations} agencies"
    ax.text(pos[company][0], pos[company][1] - 1.5, investigation_text,
            fontsize=12, ha='center', fontweight='bold', fontproperties=orbitron_font, color="black")

# Add agency abbreviations to the left of the agency logos
for agency, abbreviation in agency_abbreviations.items():
    ax.text(pos[agency][0] - 0.25, pos[agency][1], abbreviation, fontsize=12, ha='right', fontweight='bold',
            fontproperties=orbitron_font, color="black")

# Set final title and display
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-len(agency_logos) * y_spacing - 4, 3)  
ax.axis("off")
ax.set_title("Government Agencies Investigating Musk-Led Companies", fontsize=18, fontweight="bold", 
             fontproperties=orbitron_font, color="black")

plt.show()
