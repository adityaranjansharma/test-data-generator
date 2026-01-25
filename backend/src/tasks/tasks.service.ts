import { Injectable, Logger } from '@nestjs/common';
import { Cron, CronExpression } from '@nestjs/schedule';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class TasksService {
  private readonly logger = new Logger(TasksService.name);

  constructor(private prisma: PrismaService) {}

  @Cron(CronExpression.EVERY_30_SECONDS)
  async handleLeaseExpiration() {
    this.logger.debug('Checking for expired leases...');

    const now = new Date();

    // Find expired records first to log them
    const expiredRecords = await this.prisma.record.findMany({
      where: {
        status: 'leased',
        leaseExpiresAt: {
          lt: now,
        },
      },
    });

    if (expiredRecords.length > 0) {
      // Update them
      await this.prisma.record.updateMany({
        where: {
          id: { in: expiredRecords.map(r => r.id) }
        },
        data: {
          status: 'available',
          leaseExpiresAt: null,
          leasedBy: null,
        },
      });

      // Log audits
      await this.prisma.auditLog.createMany({
        data: expiredRecords.map(r => ({
          recordId: r.id,
          action: 'expired',
          actor: 'system',
          timestamp: now
        }))
      });

      this.logger.log(`Reset ${expiredRecords.length} expired records to available.`);
    }
  }
}
