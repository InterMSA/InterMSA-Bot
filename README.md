# interMSA
a discord bot that verifies members across the proffesional-prep server for college student
<div id="top"></div>

<!-- [![Contributors][contributors-shield]][contributors-url] -->
<!-- [![Forks][forks-shield]][forks-url] -->
[![Stargazers][stars-shield]][stars-url]
<!-- [![Issues][issues-shield]][issues-url] -->
<!-- [![MIT License][license-shield]][license-url] -->
<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/InterMSA/InterMSA-Bot">
    <img src="https://intermsa.com/assets/images/intermsa.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">inter-MSA Discord Bot</h3>

  <p align="center">
    A discord bot that verifies members across the proffesional-prep server for college student.
    <br />
    <a href="https://github.com/InterMSA/InterMSA-Bot"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://www.youtube.com/watch?v=YVMIskPFfUM">View Demo</a>
    ·
    <a href="https://github.com/InterMSA/InterMSA-Bot/issues">Report Bug</a>
    ·
    <a href="https://github.com/InterMSA/InterMSA-Bot/issues">Request Feature</a>
  </p>
</div>



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
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


It was an obstacle to creating a safe community where people could network safely in a professional environment knowing the person’s name and some background. This discord aims to organize people on different channels, so far it manages students in 11+ different universities with over 300 students who have used it. 


Why?
* Avoid spam 
* Organizes users into different channels
* divides the server into Ladies to connect together, Men together, and a moderated mixed channel for hiring purposes 

If you are looking for a discord bot customized for your MSA (Muslim Student Association Club) then feel free to look into this code and take inspiration from it

If you want to use the scrapping version of this bot to get the emails and names of students from your university and ensure the person is 100% in your college you may look into the [older version of the bot](https://github.com/InterMSA/InterMSA-Bot/tree/084d42f9f6b75951e344566fd468688367c50cce) and run put.py

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

 Major frameworks/libraries I used to bootstrap my project. 

* [Python](https://docs.python.org/3/tutorial/)
* [Discord.py2.0](https://github.com/Rapptz/discord.py)
* [Sqlite](https://www.sqlite.org/index.html)
* [Google Cloud Platform](https://cloud.google.com/)

<p align="right">(<a href="#top">back to top</a>)</p>


## Prerequisites
1) Make sure you have a token under folder named secrets ... (view file key.py)
2) Make sure to configure config.py to be same settings (channel ID) as your server
3) review screenshot bellow to see how the server is structured. 


- Create Server
- Create Brother/Sister, Owner, Waiting oom roles role
- Create #verify chat
- Create waiting rooms
- Create Bro/Sis Categories
- Set Perms
- Enable Developer Mode
  Copy ID's:
  - Right click on Server Name
  - Right click on #verify chat
  - Right click on #general chats for brothers & sisters
- Make @everyone role only able to talk in #verify chat
- Remove all permissions from @everyone role except for send messages

<div align="center">
  <img src="https://media.discordapp.net/attachments/1038123706830049335/1065172440193433642/image.png?width=1254&height=632">
  <img src="https://media.discordapp.net/attachments/1038123706830049335/1065173042298368020/image.png">
   <img src="https://cdn.discordapp.com/attachments/1038123706830049335/1065183898448965692/image.png">
</div>


<!-- GETTING STARTED -->
## Getting Started
To start the bot, run main.py

Type `>cmds` and you will get the appropriate commands to use
Type `>ask` in the verify channel and you will get the modal or form so people can verify from there 


### Commands
**>`cmds`** | Show every valid command

**roll a dice**

**flip a coin**

**`ws`** | Walaikumu Salam

**>quote** | get some wisdom

**>8** ask the ball yes/no question

**>choose** pick between multiple options

**>colour** will give you dropdown FAQ


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] add readME
- [x] Host in GCP 
- [ ] use git command to debug the bot/update/restart it from discord
- [ ] demo video 


Check out [open issues](https://github.com/InterMSA/InterMSA-Bot/issues) to see any proposed features AKA issues.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

This entire program is open srouce so feel free to take inspiration from it. Also please feel free to suggest any great ideas. No idea is left behind :) You may please fork the repo and create a pull request. 
Feel free to give this project a star if you like it. 

To add your changes using Git:
1. Fork the Project
2. Create your Feature Branch (`git checkout -b cool/AmazingIdea`)
3. Commit your Changes (`git commit -m 'Add some AmazingIdea'`)
4. Push to the Branch (`git push origin feature/AmazingIdea`)
5. Open a Pull Request

You can also download Github Desktop to use GUI system to do similar function to the top

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Baraa Nassar - [@baraa2nassar](https://www.instagram.com/baraa2nassar) - baraa-aziz@hotmail.com

Project Link: [https://github.com/InterMSA/InterMSA-Bot](https://github.com/InterMSA/InterMSA-Bot)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Some other sources that helped me build this project:

* [Discord.py reference library](https://github.com/Rapptz/discord.py)
* [RibiDanny Github](https://github.com/Rapptz/RoboDanny)
* [discord.py server]

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-url]: https://github.com/InterMSA/InterMSA-Bot/graphs/contributors

[forks-url]: https://github.com/InterMSA/InterMSA-Bot/network/members

[stars-url]: https://github.com/InterMSA/InterMSA-Bot/stargazers
[issues-url]: https://github.com/InterMSA/InterMSA-Bot/issues
[license-url]: https://github.com/InterMSA/InterMSA-Bot/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[product-screenshot]: https://cdn.discordapp.com/attachments/767632792950407179/929123702036107324/unknown.png
