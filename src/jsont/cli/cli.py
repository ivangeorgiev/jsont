if True: # pragma: no cover
    import io
    import sys
    import json
    import csv
    import click
    from jsont import create_path_map, map_rows, get_deep_attr

    @click.group()
    def cli():
        pass

    @cli.group(name='convert')
    def cli_convert():
        pass


    @cli_convert.group(name='json')
    def cli_convert_json():
        pass

    @cli_convert_json.group(name='to')
    def cli_convert_json_to():
        pass


    @cli_convert_json_to.command(name='csv', help='Convert JSON file to CSV')
    @click.option('--input-file', '-i', help='Path to the input file. If not specified, standard input is used')
    @click.option('--output-file', '-o', help='Path to the output file. If not specified, standard output is used')
    @click.option('--mapping-file', '-m', required=True, help='Path to the mapping file')
    def cli_convert_json_to_csv(input_file, output_file, mapping_file):
        with open(mapping_file, 'r') as mf:
            mapping_def = json.load(mf)
        if input_file:
            with open(input_file, 'r') as infile:
                input_data = json.load(infile)
        else:
            input_data = json.load(sys.stdin)

        mapping = create_path_map(mapping_def['field_map'], default='')
        root_path = get_deep_attr(mapping_def, 'root/path', default='')
        mapped = map_rows(input_data, map=mapping, root=root_path)
        fields_names = mapping_def['field_map'].keys()
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        if mapping_def.get('header_row', True):
            writer.writerow(fields_names)
        for row in mapped:
            values = [row[field_name] for field_name in fields_names]
            writer.writerow(values)
        output = buffer.getvalue()
        output = output.replace('\r\n', '\n')
        output = output.replace('\n\n', '\n')
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(output)
        else:
            sys.stdout.write(output)
