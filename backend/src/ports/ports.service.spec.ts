import { PrismaService } from '../prisma/prisma.service';
import { Test, TestingModule } from '@nestjs/testing';
import { PortsService } from './ports.service';

describe('PortsService', () => {
  let service: PortsService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        PortsService,
        {
          provide: PrismaService,
          useValue: {}, // Mock PrismaService
        },
      ],
    }).compile();

    service = module.get<PortsService>(PortsService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
