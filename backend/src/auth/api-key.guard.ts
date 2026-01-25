import { CanActivate, ExecutionContext, Injectable, UnauthorizedException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class ApiKeyGuard implements CanActivate {
  constructor(private prisma: PrismaService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const apiKey = request.headers['x-api-key'];

    if (!apiKey) {
      throw new UnauthorizedException('API Key missing');
    }

    const keyRecord = await this.prisma.apiKey.findUnique({
      where: { key: apiKey as string },
      include: { owner: true },
    });

    if (!keyRecord || !keyRecord.active) {
      throw new UnauthorizedException('Invalid or inactive API Key');
    }

    // Attach user/key to request
    request['user'] = keyRecord.owner;
    request['apiKey'] = keyRecord;

    return true;
  }
}
