import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient({});

async function main() {
  const user = await prisma.user.create({
    data: {
      name: 'Default User',
      type: 'human',
    },
  });

  const apiKey = await prisma.apiKey.create({
    data: {
      key: 'secret-key-123',
      ownerId: user.id,
      permissions: 'all',
    },
  });

  console.log({ user, apiKey });
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
