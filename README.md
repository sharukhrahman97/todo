# TODO App - PESTO Take Home Assessment
_Sharukh Rahman S_ -> [Portfolio](https://sharukhrahman.vercel.app/)

The application will allow users to create, update, and delete tasks. Tasks should have a title, description, and a status (e.g., "To Do," "In Progress," "Done"). Users should also be able to view a list of tasks and filter them by status.

>Wish to see the documentation for API's visit [here](https://documenter.getpostman.com/view/11698155/2sA3Qs9rep)

## Getting started

Better to use nvm lts! I'm using node version 20.12.2

To run the app use the commands below
Open 2 terminals

terminal 1
```
cd backend
npm i
npx prisma migrate dev --name init
npm run dev
```
terminal 2
```
cd frontend
npm i
npm run dev
```

>frontend will run in [localhost:5173](http://localhost:5173/)
>frontend will run in [localhost:5000](http://localhost:5000/)

Note: I have also attached the postman collection file too!
