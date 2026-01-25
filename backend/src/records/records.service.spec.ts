import { PrismaService } from '../prisma/prisma.service';
import { Test, TestingModule } from '@nestjs/testing';
import { RecordsService } from './records.service';

describe('RecordsService', () => {
  let service: RecordsService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        RecordsService,
        {
          provide: PrismaService,
          useValue: {},
        },
      ],
    }).compile();

    service = module.get<RecordsService>(RecordsService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
