
  <h3 align="center">Tennis API</h3>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
This API attempts to tackle the problem of the lack of ability to retrieve live ATP information as well as document racquets and/or strings in the market.

Using web scraping to extract data from the official ATP website, users are able to hit endpoints to retrieve information such as current rankings, tennis statistics such as top servers, and the top tennis players of all time. 

Along wth the ATP information, tennis players are able to create a collaborative approach to keeping track of tennis racquets by inserting and reading tennis racquet specification information from an open database. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

The tennis API was built with the below toolsa and frameworks

* FLASK
* MySQL
* Jason Web Tokens
* Swagger
* Docker
* Microsoft Azure

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps below:

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* install Python e.g., Ubuntu
  ```sh
  sudo apt-get install python3-dev python3-pip
  ```

### Installation

Below is how you could get the api running locally on your device.

1. Clone the repository
2. Install necessary libraries
   ```sh
   pip3 install -r requirements.txt
   ```
3. Create local MySQL
   ```sh
   Create Database tennisapi
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage
1. Register an acccount
2. After loggin in you will be able to access the various endpoints with the bearer authorization token that the client recieves in the response. 
3. Send POST requests to insert into the racquet catalog or even requests the current ATP tennis rankings. The options are endless!


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes 
4. Push to the Branch 
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Jacob Lapkin - jacobglapkin@gmail.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<p align="right">(<a href="#readme-top">back to top</a>)</p>
