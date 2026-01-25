export class CreatePortDto {
  name: string;
  environment?: string;
  maxRecords?: number;
  leaseTimeoutSeconds?: number;
  accessLevel?: string;
}
