import { ApiKeyGuard } from '../auth/api-key.guard';
import { PrismaService } from '../prisma/prisma.service';
import { RecordsService } from './records.service';
import { Test, TestingModule } from '@nestjs/testing';
import { RecordsController } from './records.controller';

describe('RecordsController', () => {
  let controller: RecordsController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [RecordsController],
      providers: [
        {
          provide: RecordsService,
          useValue: {},
        },
        {
          provide: PrismaService,
          useValue: {},
        }
      ],
    })
      .overrideGuard(ApiKeyGuard)
      .useValue({ canActivate: () => true })
      .compile();

    controller = module.get<RecordsController>(RecordsController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
