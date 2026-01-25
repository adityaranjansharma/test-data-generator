import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class RecordsService {
  constructor(private prisma: PrismaService) {}

  async createRecord(portName: string, ownerId: number, data: any) {
    const port = await this.prisma.port.findFirst({
      where: { name: portName, ownerId },
    });
    if (!port) throw new NotFoundException('Port not found');

    const dataToStore = typeof data === 'string' ? data : JSON.stringify(data);

    const record = await this.prisma.record.create({
      data: {
        portId: port.id,
        data: dataToStore,
        status: 'available',
      },
    });
    return this.mapRecord(record);
  }

  async leaseRecord(portName: string, ownerId: number) {
    const port = await this.prisma.port.findFirst({
      where: { name: portName, ownerId },
    });
    if (!port) throw new NotFoundException('Port not found');

    const leaseTime = new Date(Date.now() + port.leaseTimeoutSeconds * 1000);
    let leasedRecord = null;

    try {
      // Postgres implementation
      const result: any[] = await this.prisma.$queryRaw`
        UPDATE records
        SET status = 'leased', lease_expires_at = ${leaseTime}, leased_by = 'api'
        WHERE id = (
          SELECT id FROM records
          WHERE port_id = ${port.id} AND status = 'available'
          LIMIT 1
          FOR UPDATE SKIP LOCKED
        )
        RETURNING id, port_id, data, status, lease_expires_at
      `;

      if (result.length > 0) {
        leasedRecord = this.mapRecord(result[0]);
      }
    } catch (e) {
      // SQLite fallback (Dev only)
      leasedRecord = await this.prisma.$transaction(async (tx) => {
        const record = await tx.record.findFirst({
            where: { portId: port.id, status: 'available' }
        });
        if (!record) return null;
        const updated = await tx.record.update({
            where: { id: record.id },
            data: { status: 'leased', leaseExpiresAt: leaseTime, leasedBy: 'api' }
        });
        return this.mapRecord(updated);
      });
    }

    if (leasedRecord) {
      await this.prisma.auditLog.create({
        data: {
          recordId: Number(leasedRecord.id),
          action: 'leased',
          actor: 'api' // or user info if passed
        }
      });
    }

    return leasedRecord;
  }

  async consumeRecord(id: string) {
    const record = await this.prisma.record.update({
      where: { id: Number(id) },
      data: { status: 'consumed', leaseExpiresAt: null },
    });

    await this.prisma.auditLog.create({
        data: {
            recordId: record.id,
            action: 'consumed',
            actor: 'api'
        }
    });

    return this.mapRecord(record);
  }

  async releaseRecord(id: string) {
    const record = await this.prisma.record.update({
      where: { id: Number(id) },
      data: { status: 'available', leaseExpiresAt: null, leasedBy: null },
    });

    await this.prisma.auditLog.create({
        data: {
            recordId: record.id,
            action: 'released',
            actor: 'api'
        }
    });

    return this.mapRecord(record);
  }

  private mapRecord(record: any) {
      return {
          ...record,
          id: record.id.toString(),
          data: typeof record.data === 'string' ? JSON.parse(record.data) : record.data,
          // Handle mixed snake_case (raw query) vs camelCase (prisma client)
          leaseExpiresAt: record.leaseExpiresAt || record.lease_expires_at,
          portId: record.portId || record.port_id
      };
  }
}
