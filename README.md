# Strava Activity Poster Generator

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

The Strava Activity Poster Generator is a project that takes Strava data exported by the user and creates posters with all the activities. This allows users to visualize their activities in a visually appealing and personalized way.

![Image Sample](image%20sample/planche.jpg)

## Table of Contents

- [Introduction](#introduction)
- [Exporting Data from Strava](#exporting-data-from-strava)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Strava Activity Poster Generator is a Python-based project that leverages Strava data to generate posters. The project utilizes the GPX files and an `activities.csv` file exported from Strava to create personalized posters that display key details of each activity.

## Exporting Data from Strava

To export your data from Strava, follow these steps:

1. Log in to your Strava account.
2. Go to [www.strava.com](https://www.strava.com) and navigate to your profile page.
3. Click on "Dashboard" in the top menu.
4. On the left sidebar, click on "Settings."
5. Under the "My Profile" section, click on "Download or Delete Your Account."
6. On the "Download Your Account" page, click on "Request Your Archive."
7. Strava will send you an email with a download link. Click on the link in the email to download your data.
8. Extract the downloaded ZIP file to access your exported data.

## Usage

To use the Strava Activity Poster Generator, follow these steps:

1. Clone this repository to your local machine.

   ```bash
   git clone https://github.com/Pataclop/GPX.git
   ```

2. Copy the .zip file from Strava to the root directory of the project.

4. Run main script and use the interface

   ```bash
   python3 main.py
   ```
You will have to choose a year, and later the number of columns and rows of the poster

5. The generated posters will be saved in the project directory, individual images in the IMAGES directory.

## Contributing

Contributions to the Strava Activity Poster Generator project are welcome! If you have any ideas, suggestions, or bug reports, please open an issue on the GitHub repository. If you would like to contribute code, you can fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the terms of the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute this project in accordance with the license agreement.
