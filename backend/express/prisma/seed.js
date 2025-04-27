const { PrismaClient } = require('@prisma/client')
const { generateSalt, hashPassword } = require("../src/util/password.util")

const prisma = new PrismaClient()

const userData = [
  {
    id: '123',
    email: 'alice@gmail.com',
    password: "1234",
    name: 'Alice',
    todos: {
      create: [
        {
          title: 'Check this out',
          description: 'Elit consectetur tempor nostrud nisi ad fugiat sint proident voluptate. Enim incididunt ullamco laboris commodo dolore ipsum aute ea. Laboris nulla ullamco nulla aliqua sit officia culpa dolore magna pariatur do excepteur ea irure. Cillum do consequat ipsum esse exercitation qui qui nostrud magna dolor. Laborum aute aliqua nisi commodo ut consequat excepteur irure nulla sunt qui qui sint. Sunt eiusmod officia duis ut amet dolor consectetur elit elit. Voluptate incididunt exercitation cupidatat officia ea laborum aute cillum reprehenderit laboris.',
          status: "TODO",
        },
      ],
    },
  },
]

async function main() {
  console.log(`Start seeding ...`)
  for (const u of userData) {
    const { salt, hashedPassword } = hashPassword(u.password, generateSalt())
    u.salt = salt
    u.hashedPassword = hashedPassword
    delete u.password
    const user = await prisma.user.create({
      data: u,
    })
    console.log(`Created user with id: ${user.id}`)
  }
  console.log(`Seeding finished.`)
}

main()
  .then(async () => {
    await prisma.$disconnect()
  })
  .catch(async (e) => {
    console.error(e)
    await prisma.$disconnect()
    process.exit(1)
  })
