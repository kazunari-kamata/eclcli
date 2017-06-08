from eclcli.common import command
from eclcli.common import utils
from ..networkclient.common import utils as to_obj


class ListQosOption(command.Lister):
    def get_parser(self, prog_name):
        parser = super(ListQosOption, self).get_parser(prog_name)
        parser.add_argument(
            '--name',
            metavar="name",
            help="filter by name")
        parser.add_argument(
            '--qos-type',
            metavar="qos_type",
            help="filter by qos_type: besteffort, guaranteed")
        parser.add_argument(
            '--service-type',
            metavar="service_type",
            help="filter by service_type: aws, interdc, internet, vpn")
        parser.add_argument(
            '--aws-service-id',
            metavar="aws_service_id",
            help="filter by aws service id")
        parser.add_argument(
            '--interdc-service-id',
            metavar="interdc_service_id",
            help="filter by interdc service id")
        parser.add_argument(
            '--internet-service-id',
            metavar="internet_service_id",
            help="filter by internet service id")
        parser.add_argument(
            '--vpn-service-id',
            metavar="vpn_service_id",
            help="filter by vpn service id")
        parser.add_argument(
            '--status',
            metavar="status",
            help="filter by status")
        parser.add_argument(
            '--bandwidth',
            metavar="bandwidth",
            help="filter by bandwidth")
        return parser

    def take_action(self, parsed_args):
        network_client = self.app.client_manager.network
        columns = (
            'id',
            'name',
            'qos_type',
            'service_type',
            'status',
        )
        column_headers = (
            'ID',
            'Name',
            'QoS Type',
            'Service Type',
            'Status',
        )
        params = dict()
        if parsed_args.name:
            params.update({"name": parsed_args.name})
        if parsed_args.service_type:
            params.update({"service_type": parsed_args.service_type})
        if parsed_args.qos_type:
            params.update({"qos_type": parsed_args.qos_type})
        if parsed_args.aws_service_id:
            params.update({"aws_service_id": parsed_args.aws_service_id})
        if parsed_args.interdc_service_id:
            params.update({"interdc_service_id": parsed_args.interdc_service_id})
        if parsed_args.internet_service_id:
            params.update({"internet_service_id": parsed_args.internet_service_id})
        if parsed_args.vpn_service_id:
            params.update({"vpn_service_id": parsed_args.vpn_service_id})
        if parsed_args.status:
            params.update({"status": parsed_args.status})
        if parsed_args.bandwidth:
            params.update({"bandwidth": parsed_args.bandwidth})

        data = [to_obj.QosOption(inetsv)
                for inetsv in network_client.list_qos_options(
                    **params).get('qos_options')]

        return (column_headers,
                (utils.get_item_properties(
                    s, columns,
                ) for s in data))


class ShowQosOption(command.ShowOne):
    def get_parser(self, prog_name):
        parser = super(ShowQosOption, self).get_parser(prog_name)
        parser.add_argument(
            'qos_option_id',
            metavar="QOS_OPTION_ID",
            help="ID of QoS Option to show."
        )
        return parser

    def take_action(self, parsed_args):
        network_client = self.app.client_manager.network

        qos_id = parsed_args.qos_option_id

        dic = network_client.show_qos_option(qos_id).get('qos_option')
        columns = utils.get_columns(dic)
        obj = to_obj.QosOption(dic)
        data = utils.get_item_properties(
            obj, columns,)
        return columns, data
