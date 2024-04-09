# An Application for Algorithmic Textual Comparison


## Running the Project

The project is bundled and packaged as containers. These are required to run the project:

- [Docker installation](https://docs.docker.com/engine/install/)
- A Terminal:
    - Windows: Use one of these: [Windows Terminal](https://aka.ms/terminal), PowerShell, CMD
    - Linux: Anyone using Linux knows where it is.
    - MacOS: Press Command+Space, then type Terminal.
- Internet connection: To download pre-built images.

### Initial One-time Steps
A persistent volume for database data must be created once:

```shell
docker volume create idp-postgres-data
```

This volume is stored on your local device.

### Running The Project

```shell
docker-compose up -d
```

Note that the project runs in your background. It needs to be stopped to free up system resources.

```
docker-compose down
```

## Getting More, Going Advanced

### Use of local builds instead of pre-built versions
We use `docker-compose` to build multiple containers and ensure inter-connectivity among them. For better performance, we have pre-built several packages. To use your own built images, go to [docker-compose.yml](docker-compose.yml) file, comment out lines starting with `image: ghcr.io...`, then uncomment their following lines.

After doing this, you can build and run:

```shell
docker-compose up -d --build
```

### Deleting all local data

```shell
docker-compose down
docker volume rm idp-postgres-data
```

### CUDA enabled builds

Nvidia's CUDA library enables GPU acceleration. `torch` dependency of the backend can be installed with CUDA packages as well. In this case, the build size will be much larger, possibly around 12 GB for the backend. Follow the following steps:

1. First, go to [backend/pyproject.toml](backend/pyproject.toml) file and find lines starting with `torch`.
2. Comment out CUDA-enabled line, whereas comment in the current one.
3. Run the following on terminal:

```shell
poetry lock
```

4. Build the `backend` image:

```shell
docker build -t tum_idp_backend:latest --platform linux/amd64 --no-cache .
```

5. Update [docker-compose.yml](docker-compose.yml) file by referring local builds subsection of this document.

6. Run it.

### User Manual
1. **Accessing the Sign In Page:** To access the sign-in page, open your web browser and enter the URL of the application. You will be redirected to the sign-in page automatically.

![Sign In Page](figures/Login.png)

2. **Entering Credentials:** Provide your username and password on the sign-in page.

3. **Authentication Process:** Click on the "Sign In" button to initiate the authentication process.

4. **Accessing System Features:** Upon successful authentication, you can navigate through different pages and perform various actions within the application.

5. **Session Management:** Ensure to log out after completing your tasks.

### Use Cases
- **User Login:** Accessing comparative analysis features by signing in.

### Dashboard

#### Description
The dashboard provides users with an overview of key information and insights related to the system's data and functionality.

#### Features
- **Overview of data collection**
- **Graphical representations of data**

#### User Manual
1. **Accessing the Dashboard:** Log in to the system to access the dashboard.

![Dashboard](figures/Dashboard.png)

2. **Graphical Representations of Data:** Data on the dashboard is presented in various graphical formats.

3. **Interacting with Data:** Users can interact with the data displayed on the dashboard.

#### Use Cases
- **Real-time Insights:** Monitoring industry distribution among companies.

### Database Management

#### Description
Database management facilitates efficient handling and organization of data.

#### Features
- **Viewing and Editing Database Entries**
- **Search and Filter Capabilities**
- **Data Export Option**

#### User Manual
1. **Viewing Database Entries:** Select the table and click "Run" to view entries.

![Database Management](figures/DBManagementEmpty.png)

2. **Search and Filter Capabilities:** Use search bar or filter options.

![Query Search](figures/DBManagementQuerySearch.png)

3. **Editing Database Entries:** Click "Edit" to modify entries.

4. **Importing Data into Database:** Click "Import Data" and select JSON file to import.

5. **Deleting a Document:** Select entry and click "Delete" to remove.

#### Use Cases
- **Data Entry Modification**
- **Search for Specific Data**
- **Export Data for Analysis**

### Similarity Analysis

#### Description
Compare textual data, particularly Ten-K documents, based on their business descriptions.

#### Features
- **Text Analysis Tab**
- **Parameter Selection**
- **Cosine Similarity Measurement**
- **Top Similar Documents Retrieval**

![Similarity](figures/SimilarityEmpty.png)

#### User Manual
1. **Accessing the Similarity Analysis Tab:** Navigate to the text analysis tab.

2. **Selecting Parameters:** Choose similarity analysis option and specify parameters.

3. **Submitting the Query:** Press the submit button.

4. **Viewing Results:** View top 10 similar documents based on cosine similarity scores.

![Similarity Results](figures/SimilarityResults.png)

#### Use Cases
- **Comparing Text Queries**
- **Analyzing Historical Trends**

### Clustering

#### Description
Clustering identifies groups of similar data points within a dataset.

#### Features
- **Grouping of Similar Data Points**
- **Interactive Visualization of Clusters**

![Clustering](figures/ClusteringEmpty.png)

#### User Manual
1. **Running Clustering Algorithm:** Navigate to clustering section and choose parameters.

2. **Exploring Cluster Results:** Use interactive visualization tool to explore clusters.

![Clustering Graphic](figures/ClusteringGraphic.png)

#### Use Cases
- **Identifying Business Themes**
- **Benchmarking Competitors**

### User Management

#### Description
User management ensures a seamless and intuitive experience for users interacting with the system.

#### Features
- **Intuitive UI Design**
- **Smooth Transition Between Pages**
- **Feedback Mechanisms for User Actions**

![User Management](figures/UserManagementEmpty.png)

#### User Manual
1. **Adding a User:** Click "Add User" and provide necessary details.

![Add User](figures/AddUser.png)

2. **Editing a User:** Click "Edit" next to user profile and update information.

![Edit User](figures/EditUser.png)

3. **Deleting a User:** Select user and click "Delete" to remove.

![Delete User](figures/DeleteUser.png)

#### Use Cases
- **Adding a New User**
- **Editing User Information**
- **Deleting an Inactive User**

