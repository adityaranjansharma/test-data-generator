import { Controller, Get, Post, Body, UseGuards, Req, Param } from '@nestjs/common';
import { PortsService } from './ports.service';
import { CreatePortDto } from './dto/create-port.dto';
import { ApiKeyGuard } from '../auth/api-key.guard';

@Controller('api/ports')
@UseGuards(ApiKeyGuard)
export class PortsController {
  constructor(private readonly portsService: PortsService) {}

  @Post()
  create(@Req() req: any, @Body() createPortDto: CreatePortDto) {
    return this.portsService.createPort(req.user.id, createPortDto);
  }

  @Get()
  findAll(@Req() req: any) {
    return this.portsService.getPorts(req.user.id);
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.portsService.getPortById(id);
  }
}
