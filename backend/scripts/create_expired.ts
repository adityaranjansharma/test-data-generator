import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  const user = await prisma.user.findFirst();
  const port = await prisma.port.create({
    data: {
      name: 'expiry-test-port',
      ownerId: user!.id,
    }
  });

  const record = await prisma.record.create({
    data: {
      portId: port.id,
      data: '{"test":"expiry"}',
      status: 'leased',
      leaseExpiresAt: new Date(Date.now() - 10000), // Expired 10s ago
      leasedBy: 'tester'
    }
  });

  console.log('Created expired record:', record.id);
}

main().finally(() => prisma.$disconnect());
