import { Controller, Post, Body, Param, UseGuards, Req, NotFoundException, HttpException, HttpStatus } from '@nestjs/common';
import { RecordsService } from './records.service';
import { CreateRecordDto } from './dto/create-record.dto';
import { ApiKeyGuard } from '../auth/api-key.guard';

@Controller('api')
@UseGuards(ApiKeyGuard)
export class RecordsController {
  constructor(private readonly recordsService: RecordsService) {}

  @Post('ports/:portName/records')
  create(@Req() req: any, @Param('portName') portName: string, @Body() createDto: CreateRecordDto) {
    return this.recordsService.createRecord(portName, req.user.id, createDto.data);
  }

  @Post('ports/:portName/records/lease')
  async lease(@Req() req: any, @Param('portName') portName: string) {
    const record = await this.recordsService.leaseRecord(portName, req.user.id);
    if (!record) {
      throw new HttpException('No records available', HttpStatus.NOT_FOUND);
    }
    return {
      recordId: record.id,
      data: record.data
    };
  }

  @Post('records/:id/consume')
  consume(@Param('id') id: string) {
    return this.recordsService.consumeRecord(id);
  }

  @Post('records/:id/release')
  release(@Param('id') id: string) {
    return this.recordsService.releaseRecord(id);
  }
}
