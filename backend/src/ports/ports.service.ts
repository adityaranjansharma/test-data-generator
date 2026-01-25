import { Injectable, ConflictException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreatePortDto } from './dto/create-port.dto';
import { Prisma } from '@prisma/client';

@Injectable()
export class PortsService {
  constructor(private prisma: PrismaService) {}

  async createPort(userId: number, dto: CreatePortDto) {
    try {
      return await this.prisma.port.create({
        data: {
          name: dto.name,
          environment: dto.environment,
          maxRecords: dto.maxRecords,
          leaseTimeoutSeconds: dto.leaseTimeoutSeconds,
          accessLevel: dto.accessLevel,
          owner: { connect: { id: userId } },
        },
      });
    } catch (error) {
      if (error instanceof Prisma.PrismaClientKnownRequestError) {
        if (error.code === 'P2002') {
          throw new ConflictException('Port name already exists for this owner and environment');
        }
      }
      throw error;
    }
  }

  async getPorts(userId: number) {
    return this.prisma.port.findMany({
      where: { ownerId: userId },
      orderBy: { createdAt: 'desc' },
      include: {
        _count: {
          select: { records: true }
        }
      }
    });
  }

  async getPortById(id: string) {
    return this.prisma.port.findUnique({
      where: { id },
      include: {
        _count: {
          select: { records: true }
        }
      }
    });
  }
}
