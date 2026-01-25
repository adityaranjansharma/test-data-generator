import { ApiKeyGuard } from '../auth/api-key.guard';
import { PrismaService } from '../prisma/prisma.service';
import { PortsService } from './ports.service';
import { Test, TestingModule } from '@nestjs/testing';
import { PortsController } from './ports.controller';

describe('PortsController', () => {
  let controller: PortsController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [PortsController],
      providers: [
        {
          provide: PortsService,
          useValue: {},
        },
        {
          provide: PrismaService, // Guard needs this if it uses it, but controller uses guard?
          useValue: {},
        }
      ],
    })
      .overrideGuard(ApiKeyGuard) // Mock guard to avoid Prisma dependency
      .useValue({ canActivate: () => true })
      .compile();

    controller = module.get<PortsController>(PortsController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
