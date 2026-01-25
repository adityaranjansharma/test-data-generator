import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { AuthModule } from './auth/auth.module';
import { PortsModule } from './ports/ports.module';
import { RecordsModule } from './records/records.module';
import { PrismaModule } from './prisma/prisma.module';
import { TasksModule } from './tasks/tasks.module';
import { ScheduleModule } from '@nestjs/schedule';
import { ThrottlerModule, ThrottlerGuard } from '@nestjs/throttler';
import { APP_GUARD } from '@nestjs/core';
import { ApiKeyThrottlerGuard } from './auth/api-key-throttler.guard';

@Module({
  imports: [
    ScheduleModule.forRoot(),
    ThrottlerModule.forRoot([{
      ttl: 60000,
      limit: 1000, // 1000 reqs per minute per key
    }]),
    AuthModule,
    PortsModule,
    RecordsModule,
    PrismaModule,
    TasksModule
  ],
  controllers: [AppController],
  providers: [
    AppService,
    {
      provide: APP_GUARD,
      useClass: ApiKeyThrottlerGuard,
    },
  ],
})
export class AppModule {}
