def generate_analysis_report(data_csv, comparison_data=None, output_dir=None, return_images_as_b64=False):
    """
    Generate AI content analysis report with visualizations
    
    Parameters:
    -----------
    data_csv : str
        CSV data containing comparison metrics. Can be:
        - A string containing CSV data
        - A path to a CSV file
        Expected format is a CSV with columns: Comparison, Metric, High-B, Base, Delta
        
    comparison_data : str or None
        Not used in this version - included for backward compatibility
        
    output_dir : str or None
        Directory where output files will be saved
        If None, files will be saved in the current directory
        
    return_images_as_b64 : bool
        If True, returns images as base64 encoded strings
        Useful for AI systems to access the image data directly
        
    Returns:
    --------
    dict
        A dictionary containing:
        - 'markdown': The markdown report text
        - 'alteration_pie': The alteration pie chart (as base64 string if return_images_as_b64=True, otherwise path)
        - 'retention_chart': The retention bar chart (as base64 string if return_images_as_b64=True, otherwise path)
    
    Raises:
    -------
    ValueError
        If data_csv is None or empty
        If required columns are missing in the CSV
        If insufficient data is available for visualization
    """
    
    # Check if data is provided
    if not data_csv:
        raise ValueError("CSV data is required. Please provide CSV data as a string or file path.")
    
    # Make sure the helper function exists
    def ensure_dir(directory):
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    
    # Set up output directory
    if output_dir:
        ensure_dir(output_dir)
    else:
        output_dir = "."
        
    # Handle file paths for input data
    if os.path.isfile(data_csv):
        with open(data_csv, 'r') as f:
            data_csv = f.read()
    
    # Parse the CSV data
    try:
        df = pd.read_csv(StringIO(data_csv))
    except Exception as e:
        raise ValueError(f"Failed to parse CSV data: {str(e)}")
    
    # Check for required columns in the new format
    required_columns = ['Comparison', 'Metric', 'High-B', 'Base', 'Delta']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"CSV is missing required columns: {', '.join(missing_columns)}. The CSV must include Comparison, Metric, High-B, Base, and Delta columns.")
    
    # Convert the dataframe-based format to our internal section-based format
    comp_sections = []
    for comparison in df['Comparison'].unique():
        section_data = df[df['Comparison'] == comparison]
        section = {
            'name': comparison,
            'data': []
        }
        
        for _, row in section_data.iterrows():
            section['data'].append([
                row['Metric'], 
                str(row['High-B']), 
                str(row['Base']), 
                str(row['Delta'])
            ])
        
        comp_sections.append(section)
    
    # Check if we have valid section data
    if not comp_sections:
        raise ValueError("No valid comparison sections found in the provided data. Please check your CSV format.")
    
    # Extract the stages from section names
    stages = []
    for section in comp_sections:
        parts = section['name'].split(' vs ')
        if len(parts) == 2:
            if parts[0] not in stages:
                stages.append(parts[0])
            if parts[1] not in stages:
                stages.append(parts[1])
    
    # Reorder stages to show progression
    known_stages = ["Draft (AI)", "Refined (AI-assisted)", "Edited (Human-driven)", "Final (Human)"]
    ordered_stages = []
    
    # First try to find exact matches from known stages
    for stage in known_stages:
        if stage in stages:
            ordered_stages.append(stage)
    
    # Then add any remaining stages
    for stage in stages:
        if stage not in ordered_stages:
            # Check if stage is a substring of any known stage
            matched = False
            for known in known_stages:
                if stage in known or known.split(' ')[0] in stage:
                    matched = True
                    break
            
            # Add to appropriate position based on known stages order or append at the end
            if matched:
                for i, known in enumerate(known_stages):
                    if stage in known or known.split(' ')[0] in stage:
                        if i < len(ordered_stages):
                            ordered_stages.insert(i, stage)
                        else:
                            ordered_stages.append(stage)
                        break
            else:
                ordered_stages.append(stage)
    
    # If we still don't have any stages, just use what we found
    if not ordered_stages:
        ordered_stages = stages
    
    # Check if we have valid stages
    if len(ordered_stages) < 2:
        raise ValueError("Insufficient stage data found. Please provide at least two distinct stages in your comparison data.")
    
    # Create the markdown text output
    markdown_output = "# AI Content Transformation Analysis\n\n"
    
    # 1. Content Attribution Summary
    markdown_output += "## 1. Content Attribution Summary\n\n"
    
    # Find alteration metrics for each comparison
    alt_metrics = {}
    for section in comp_sections:
        alt_data = [row for row in section['data'] if row[0] == 'Alteration %']
        if alt_data:
            try:
                alt_metrics[section['name']] = float(alt_data[0][1])  # Using High-B value
            except (ValueError, TypeError, IndexError):
                continue  # Skip if value can't be parsed
    
    # Generate attribution summary
    if alt_metrics:
        markdown_output += "| Stage Transition | Human Contribution | AI Retention |\n"
        markdown_output += "|-----------------|-------------------|-------------|\n"
        
        for transition, alteration in alt_metrics.items():
            markdown_output += f"| {transition} | {alteration:.2f}% | {100-alteration:.2f}% |\n"
    else:
        markdown_output += "No alteration metrics available in the provided data.\n"
    
    # 2. Disclosure Recommendation
    markdown_output += "\n## 2. Disclosure Recommendation\n\n"
    
    # Find the overall alteration from AI to final
    try:
        draft_to_final_alt = None
        for transition, alteration in alt_metrics.items():
            if 'Draft' in transition and 'Final' in transition:
                draft_to_final_alt = alteration
                break
                
        # If direct Draft to Final not found, estimate from available transitions
        if draft_to_final_alt is None:
            # Calculate using available transitions
            draft_to_final_alt = sum(alt_metrics.values()) / len(alt_metrics) if alt_metrics else None
    except:
        draft_to_final_alt = None
    
    if draft_to_final_alt is None:
        markdown_output += "Insufficient data to generate a disclosure recommendation. Please provide alteration metrics between Draft and Final stages.\n"
    else:
        # Generate recommended disclosure based on alteration level
        if draft_to_final_alt > 95:
            contribution_level = "minimal AI content"
        elif 80 <= draft_to_final_alt <= 95:
            contribution_level = "limited AI assistance"
        elif 50 <= draft_to_final_alt < 80:
            contribution_level = "significant human editing of AI content"
        else:
            contribution_level = "substantial AI contribution with human oversight"
        
        # Extract retention metrics
        char_retention = None
        word_retention = None
        
        # Find retention metrics from Draft to Final
        for section in comp_sections:
            if 'Draft' in section['name'] and 'Final' in section['name']:
                for row in section['data']:
                    if row[0] == 'Char Retention %':
                        try:
                            char_retention = float(row[1])  # Using High-B value
                        except (ValueError, TypeError, IndexError):
                            pass
                    elif row[0] == 'Word Retention %':
                        try:
                            word_retention = float(row[1])  # Using High-B value
                        except (ValueError, TypeError, IndexError):
                            pass
        
        # If direct metrics not found, look for any retention metrics
        if char_retention is None:
            char_retention_data = df[df['Metric'] == 'Char Retention %']
            if not char_retention_data.empty:
                char_retention = char_retention_data['High-B'].min()
        
        if word_retention is None:
            word_retention_data = df[df['Metric'] == 'Word Retention %']
            if not word_retention_data.empty:
                word_retention = word_retention_data['High-B'].min()
        
        # Only generate disclosure if we have the necessary metrics
        if char_retention is not None and word_retention is not None:
            markdown_output += f"""```
AI Assistance Disclosure: This article utilized AI tools for {contribution_level}. 
The final published version contains approximately {char_retention:.2f}% character 
retention and {word_retention:.2f}% word retention from the initial AI draft. 
All factual information, analyses, and conclusions have been verified by 
human editors who take full responsibility for the content.
```\n"""
        else:
            markdown_output += "Insufficient retention data to generate a complete disclosure. Please provide character and word retention metrics.\n"
    
    # 3. Generate Consolidated Table with Averages and Variance
    markdown_output += "\n## 3. Content Transformation Metrics\n\n"
    
    # Create a direct mapping of metrics from the DataFrame
    metrics_of_interest = ['Char Retention %', 'Word Retention %', 'Sentence Retention %', 'Paragraph Retention %']
    
    # Group data by Comparison and Metric
    metrics_by_comparison = {}
    
    for comparison in df['Comparison'].unique():
        comparison_data = df[df['Comparison'] == comparison]
        metrics_by_comparison[comparison] = {}
        
        for _, row in comparison_data.iterrows():
            metric = row['Metric']
            metrics_by_comparison[comparison][metric] = {
                'high_b': row['High-B'],
                'base': row['Base'],
                'delta': row['Delta']
            }
    
    # Extract stage names from comparisons
    stage_names = set()
    for comparison in metrics_by_comparison.keys():
        parts = comparison.split(' vs ')
        if len(parts) == 2:
            stage_names.add(parts[0])
            stage_names.add(parts[1])
    
    # Order stages based on known progression
    ordered_stages = []
    for stage in ["Draft", "Refined", "Edited", "Final"]:
        matches = [s for s in stage_names if stage in s]
        ordered_stages.extend(matches)
    
    # Add any missing stages
    for stage in stage_names:
        if stage not in ordered_stages:
            ordered_stages.append(stage)
    
    # Generate consolidated table
    if ordered_stages:
        markdown_output += "| Metric | "
        
        # Add stage headers
        for stage in ordered_stages:
            short_stage = stage.split(' ')[0] if ' ' in stage else stage
            markdown_output += f"{short_stage} : +/- | "
        
        # Add header separator
        markdown_output += "\n| " + "-" * 16 + " | "
        for _ in ordered_stages:
            markdown_output += "-" * 14 + " | "
        markdown_output += "\n"
        
        # Add rows for each metric
        for metric in metrics_of_interest:
            markdown_output += f"| {metric} | "
            
            for stage in ordered_stages:
                # Find comparison where this stage appears
                found_value = False
                found_delta = False
                value = None
                delta = None
                
                # Check comparisons where this stage is first
                for comparison, metrics in metrics_by_comparison.items():
                    parts = comparison.split(' vs ')
                    if len(parts) != 2:
                        continue
                        
                    if parts[0] == stage and metric in metrics:
                        value = metrics[metric]['high_b']
                        delta = metrics[metric]['delta']
                        found_value = True
                        found_delta = True
                        break
                
                # If not found as first stage, check as second stage
                if not found_value:
                    for comparison, metrics in metrics_by_comparison.items():
                        parts = comparison.split(' vs ')
                        if len(parts) != 2:
                            continue
                            
                        if parts[1] == stage and metric in metrics:
                            value = metrics[metric]['base']
                            delta = -metrics[metric]['delta']  # Reverse delta direction
                            found_value = True
                            found_delta = True
                            break
                
                # Format and add to table
                if found_value:
                    markdown_output += f"{value:.2f}% : "
                else:
                    markdown_output += "— : "
                    
                if found_delta:
                    if delta > 0:
                        markdown_output += f"+{delta:.2f}pp | "
                    elif delta < 0:
                        markdown_output += f"{delta:.2f}pp | "
                    else:
                        markdown_output += "0pp | "
                else:
                    markdown_output += "— | "
            
            markdown_output += "\n"
    else:
        markdown_output += "No valid stage data found for metrics table.\n"
    
    # Add a note about the visualizations
    markdown_output += "\nThe charts below visualize:\n"
    markdown_output += "1. **Content Alteration by Transformation Stage** (Pie Chart)\n"
    markdown_output += "2. **Content Retention by Transformation Stage** (Horizontal Bar Chart)\n"
    
    # Print the markdown output
    print(markdown_output)
    
    # Define output paths
    alteration_pie_path = os.path.join(output_dir, 'content_alteration_pie.png')
    retention_chart_path = os.path.join(output_dir, 'retention_bar_chart.png')
    
    # Create visualizations
    try:
        alteration_pie = create_alteration_pie_chart(comp_sections, ordered_stages, output_path=alteration_pie_path)
        retention_chart = create_retention_matrix_chart(comp_sections, ordered_stages, output_path=retention_chart_path)
    except ValueError as e:
        print(f"Warning: {str(e)}")
        alteration_pie = None
        retention_chart = None
    
    # Prepare return values
    result = {
        'markdown': markdown_output,
        'alteration_pie': alteration_pie_path if alteration_pie else None,
        'retention_chart': retention_chart_path if retention_chart else None
    }
    
    # Convert images to base64 if requested and available
    if return_images_as_b64:
        # Convert alteration pie to base64 if available
        if alteration_pie:
            flow_buffer = BytesIO()
            alteration_pie.savefig(flow_buffer, format='png', bbox_inches='tight', dpi=300)
            flow_buffer.seek(0)
            flow_b64 = base64.b64encode(flow_buffer.read()).decode('utf-8')
            result['alteration_pie'] = flow_b64
        
        # Convert retention chart to base64 if available
        if retention_chart:
            retention_buffer = BytesIO()
            retention_chart.savefig(retention_buffer, format='png', bbox_inches='tight', dpi=300)
            retention_buffer.seek(0)
            retention_b64 = base64.b64encode(retention_buffer.read()).decode('utf-8')
            result['retention_chart'] = retention_b64
    
    # Close figures to free memory
    if alteration_pie:
        plt.close(alteration_pie)
    if retention_chart:
        plt.close(retention_chart)
    
    return resultdef generate_analysis_report(data_csv, comparison_data=None, output_dir=None, return_images_as_b64=False):
    """
    Generate AI content analysis report with visualizations
    
    Parameters:
    -----------
    data_csv : str
        CSV data containing raw metrics. Can be:
        - A string containing CSV data
        - A path to a CSV file
        Required parameter - no sample data will be used
    
    comparison_data : str or None
        Markdown-formatted comparison data with deltas. Can be:
        - A string containing markdown data
        - A path to a markdown file
        If None, will be extracted from the CSV data
        
    output_dir : str or None
        Directory where output files will be saved
        If None, files will be saved in the current directory
        
    return_images_as_b64 : bool
        If True, returns images as base64 encoded strings
        Useful for AI systems to access the image data directly
        
    Returns:
    --------
    dict
        A dictionary containing:
        - 'markdown': The markdown report text
        - 'flow_diagram': The flow diagram (as base64 string if return_images_as_b64=True, otherwise path)
        - 'retention_matrix': The retention matrix chart (as base64 string if return_images_as_b64=True, otherwise path)
    
    Raises:
    -------
    ValueError
        If data_csv is None or empty
    """
    
    # Check if data is provided
    if not data_csv:
        raise ValueError("CSV data is required. Please provide CSV data as a string or file path.")
    
    # Set up output directory
    if output_dir:
        ensure_dir(output_dir)
    else:
        output_dir = "."
        
    # Handle file paths for input data
    if os.path.isfile(data_csv):
        with open(data_csv, 'r') as f:
            data_csv = f.read()
            
    if comparison_data and os.path.isfile(comparison_data):
        with open(comparison_data, 'r') as f:
            comparison_data = f.read()
    
    # Parse the CSV data
    try:
        df = pd.read_csv(StringIO(data_csv))
    except Exception as e:
        raise ValueError(f"Failed to parse CSV data: {str(e)}")
    
    # Auto-generate comparison data if not provided
    if comparison_data is None:
        comparison_data = auto_generate_comparison_data(df)
    
    # Parse the comparison data
    comp_sections = []
    current_section = None
    comp_lines = comparison_data.strip().split('\n')
    for line in comp_lines:
        if line.startswith('**'):
            if current_section:
                comp_sections.append(current_section)
            section_name = line.strip('*')
            current_section = {'name': section_name, 'data': []}
        elif ',' in line and not line.startswith('Comparison'):
            current_section['data'].append(line.split(','))
    if current_section:
        comp_sections.append(current_section)
    
    # Create a structured comparison dataframe
    comp_data = []
    for section in comp_sections:
        for row in section['data']:
            if len(row) >= 4:
                metric, high_b, base, delta = row
                comp_data.append({
                    'Section': section['name'],
                    'Metric': metric,
                    'High-B': float(high_b) if high_b and high_b != '–' else None,
                    'Base': float(base) if base and base != '–' else None,
                    'Delta': float(delta.replace('–', '-')) if delta and delta != '–' else 0
                })
    comp_df = pd.DataFrame(comp_data)
    
    # Extract the stages from section names
    stages = []
    for section in comp_sections:
        parts = section['name'].split(' vs ')
        if len(parts) == 2:
            if parts[0] not in stages:
                stages.append(parts[0])
            if parts[1] not in stages:
                stages.append(parts[1])
    
    # Reorder stages to show progression
    known_stages = ["Draft (AI)", "Refined (AI-assisted)", "Edited (Human-driven)", "Final (Human)"]
    stages = [stage for stage in known_stages if stage in stages or any(s in stage for s in stages)]
    
    # Map from the comparison data to known stages
    stage_mapping = {
        "Draft": "Draft (AI)",
        "Refined (AI-assisted)": "Refined (AI-assisted)",
        "Edited (Human-driven)": "Edited (Human-driven)",
        "Final (Human)": "Final (Human)"
    }
    
    # Create the markdown text output
    markdown_output = "# AI Content Transformation Analysis\n\n"
    
    # 1. Content Attribution Summary
    markdown_output += "## 1. Content Attribution Summary\n\n"
    
    # Calculate average alteration for each stage transition
    alt_metrics = {}
    for section in comp_sections:
        from_stage, to_stage = section['name'].split(' vs ')
        alt_data = [row for row in section['data'] if row[0] == 'Alteration %']
        if alt_data:
            alt_metrics[f"{from_stage} vs {to_stage}"] = float(alt_data[0][1])
    
    # Generate attribution summary
    markdown_output += "| Stage Transition | Human Contribution | AI Retention |\n"
    markdown_output += "|-----------------|-------------------|-------------|\n"
    
    for transition, alteration in alt_metrics.items():
        markdown_output += f"| {transition} | {alteration:.2f}% | {100-alteration:.2f}% |\n"
    
    # 2. Disclosure Recommendation
    markdown_output += "\n## 2. Disclosure Recommendation\n\n"
    
    # Find the overall alteration from AI to final
    try:
        draft_to_final_alt = max([v for k, v in alt_metrics.items() if 'Final' in k and 'Draft' in k], default=None)
        if draft_to_final_alt is None:
            # Estimate using stage transitions
            draft_to_final_alt = sum(alt_metrics.values()) / len(alt_metrics)
    except:
        draft_to_final_alt = 90  # Default if calculation fails
    
    # Generate recommended disclosure based on alteration level
    if draft_to_final_alt > 95:
        contribution_level = "minimal AI content"
    elif 80 <= draft_to_final_alt <= 95:
        contribution_level = "limited AI assistance"
    elif 50 <= draft_to_final_alt < 80:
        contribution_level = "significant human editing of AI content"
    else:
        contribution_level = "substantial AI contribution with human oversight"
    
    # Extract retention metrics
    char_retention = None
    word_retention = None
    for section in comp_sections:
        if "Final" in section['name'] and ("Draft" in section['name'] or "AI" in section['name']):
            for row in section['data']:
                if row[0] == 'Char Retention %':
                    char_retention = float(row[1])
                elif row[0] == 'Word Retention %':
                    word_retention = float(row[1])
    
    if char_retention is None:
        # Estimate from available data
        char_retention_values = [float(row[1]) for section in comp_sections for row in section['data'] if row[0] == 'Char Retention %']
        char_retention = min(char_retention_values) if char_retention_values else 10
    
    if word_retention is None:
        # Estimate from available data
        word_retention_values = [float(row[1]) for section in comp_sections for row in section['data'] if row[0] == 'Word Retention %']
        word_retention = min(word_retention_values) if word_retention_values else 25
    
    markdown_output += f"""```
AI Assistance Disclosure: This article utilized AI tools for {contribution_level}. 
The final published version contains approximately {char_retention:.2f}% character 
retention and {word_retention:.2f}% word retention from the initial AI draft. 
All factual information, analyses, and conclusions have been verified by 
human editors who take full responsibility for the content.
```\n"""
    
    # 3. Generate Consolidated Table with Averages and Variance
    markdown_output += "\n## 3. Content Transformation Metrics\n\n"
    
    # Collect metrics by stage
    metrics_of_interest = ['Char Retention %', 'Word Retention %', 'Sentence Retention %', 'Paragraph Retention %']
    stage_metrics = {}
    
    for section in comp_sections:
        from_stage, to_stage = section['name'].split(' vs ')
        
        # Initialize stages if not present
        if from_stage not in stage_metrics:
            stage_metrics[from_stage] = {metric: {'value': None, 'delta': None} for metric in metrics_of_interest}
        if to_stage not in stage_metrics:
            stage_metrics[to_stage] = {metric: {'value': None, 'delta': None} for metric in metrics_of_interest}
        
        # Extract metrics and deltas
        for row in section['data']:
            if row[0] in metrics_of_interest:
                metric = row[0]
                value = float(row[1]) if row[1] and row[1] != '–' else None
                delta = row[3] if len(row) > 3 and row[3] and row[3] != '–' else '0'
                
                # Clean delta and convert to float
                if delta.startswith('–'):
                    delta = -float(delta[1:])
                else:
                    delta = float(delta.replace('+', ''))
                
                # Assign to from_stage
                stage_metrics[from_stage][metric]['value'] = value
                stage_metrics[from_stage][metric]['delta'] = delta
    
    # Create consolidated table
    markdown_output += "| Metric | "
    
    # Add stage headers
    ordered_stages = []
    for stage in known_stages:
        if stage in stage_metrics:
            ordered_stages.append(stage)
            markdown_output += f"{stage.split(' ')[0]} : +/- | "
    
    # Add total column if we have multiple stages
    if len(ordered_stages) > 1:
        markdown_output += "Total : +/- |\n"
    else:
        markdown_output += "\n"
    
    # Add header separator
    markdown_output += "| " + "-" * 16 + " | "
    for _ in ordered_stages:
        markdown_output += "-" * 14 + " | "
    if len(ordered_stages) > 1:
        markdown_output += "-" * 10 + " |\n"
    else:
        markdown_output += "\n"
    
    # Add rows for each metric
    for metric in metrics_of_interest:
        markdown_output += f"| {metric} | "
        
        # Values for each stage
        total_value = 0
        total_delta = 0
        
        for stage in ordered_stages:
            value = stage_metrics[stage][metric]['value']
            delta = stage_metrics[stage][metric]['delta']
            
            if value is not None:
                markdown_output += f"{value:.2f}% : "
                total_value += value
            else:
                markdown_output += "— : "
            
            if delta is not None:
                if delta > 0:
                    markdown_output += f"+{delta:.2f}pp | "
                elif delta < 0:
                    markdown_output += f"{delta:.2f}pp | "
                else:
                    markdown_output += "0pp | "
                total_delta += delta
            else:
                markdown_output += "— | "
        
        # Add total column if we have multiple stages
        if len(ordered_stages) > 1:
            markdown_output += f"{total_value:.2f}% : "
            if total_delta > 0:
                markdown_output += f"+{total_delta:.2f}pp |\n"
            elif total_delta < 0:
                markdown_output += f"{total_delta:.2f}pp |\n"
            else:
                markdown_output += "0pp |\n"
        else:
            markdown_output += "\n"
    
    # Add a note about the visualizations
    markdown_output += "\nThe charts below visualize:\n"
    markdown_output += "1. **Content Alteration by Transformation Stage** (Pie Chart)\n"
    markdown_output += "2. **Content Retention by Transformation Stage** (Horizontal Bar Chart)\n"
    
    # Print the markdown output
    print(markdown_output)
    
    # Define output paths
    flow_diagram_path = os.path.join(output_dir, 'content_alteration_pie.png')
    retention_matrix_path = os.path.join(output_dir, 'retention_bar_chart.png')
    
    # Create visualizations
    flow_fig = create_alteration_pie_chart(comp_sections, stages, output_path=flow_diagram_path)
    retention_fig = create_retention_matrix_chart(comp_sections, stages, output_path=retention_matrix_path)
    
    # Prepare return values
    result = {
        'markdown': markdown_output,
        'flow_diagram': flow_diagram_path,
        'retention_matrix': retention_matrix_path
    }
    
    # Convert images to base64 if requested
    if return_images_as_b64:
        # Convert flow diagram to base64
        flow_buffer = BytesIO()
        flow_fig.savefig(flow_buffer, format='png', bbox_inches='tight', dpi=300)
        flow_buffer.seek(0)
        flow_b64 = base64.b64encode(flow_buffer.read()).decode('utf-8')
        result['flow_diagram'] = flow_b64
        
        # Convert retention matrix to base64
        retention_buffer = BytesIO()
        retention_fig.savefig(retention_buffer, format='png', bbox_inches='tight', dpi=300)
        retention_buffer.seek(0)
        retention_b64 = base64.b64encode(retention_buffer.read()).decode('utf-8')
        result['retention_matrix'] = retention_b64
    
    # Close figures to free memory
    plt.close(flow_fig)
    plt.close(retention_fig)
    
    return resultdef create_alteration_pie_chart(comp_sections, stages, output_path=None):
    """
    Create a pie chart showing alteration percentages across stages
    
    Parameters:
    -----------
    comp_sections : list
        List of comparison section data
    stages : list
        List of content stages
    output_path : str or None
        Path to save the output image
        
    Returns:
    --------
    matplotlib.figure.Figure
        The figure object
    
    Raises:
    -------
    ValueError
        If insufficient data is available to create the chart
    """
    # Extract alteration percentages for each stage transition
    alterations = []
    labels = []
    
    for i in range(len(stages) - 1):
        from_stage = stages[i]
        to_stage = stages[i+1]
        transition_label = f"{from_stage.split(' ')[0]} → {to_stage.split(' ')[0]}"
        
        # Find alteration for this transition
        for section in comp_sections:
            if all(s in section['name'] for s in [from_stage.split(' ')[0], to_stage.split(' ')[0]]):
                for row in section['data']:
                    if row[0] == 'Alteration %':
                        alterations.append(float(row[1]))
                        labels.append(transition_label)
                        break
    
    # Check if we have enough data
    if not alterations:
        raise ValueError("Insufficient alteration data available to create pie chart. Please provide alteration percentages in the input data.")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # WCAG AA compliant colors for the pie chart
    # These colors have been verified for sufficient contrast
    colors = [
        '#0072B2',  # Blue
        '#009E73',  # Green
        '#D55E00',  # Orange
        '#CC79A7',  # Pink
        '#882255'   # Purple (replacing yellow for better contrast)
    ]
    
    # Create the pie chart
    wedges, texts, autotexts = ax.pie(
        alterations, 
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors[:len(alterations)],  # Only use as many colors as we have values
        wedgeprops={'edgecolor': 'w', 'linewidth': 1},
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    
    # Add a title
    plt.title('Content Alteration by Transformation Stage', fontsize=16, pad=20)
    
    # Add a legend with the exact percentages
    legend_labels = [f"{label}: {value:.1f}%" for label, value in zip(labels, alterations)]
    plt.legend(wedges, legend_labels, title="Alteration Percentages", 
              loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.tight_layout()
    
    # Save the figure if path is provided
    if output_path:
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
    
    return fig"""
AI Content Analysis Visualization Tool

This script generates visualizations and analysis reports for AI content transformation.
It's designed to be easily executed by AI assistants with minimal setup.

Dependencies:
- matplotlib
- numpy
- pandas 
- seaborn

Usage example:
    python ai_content_analysis.py --csv_data path/to/data.csv --comparison_data path/to/comparison.md --output_dir ./outputs

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch
import matplotlib.colors as mcolors
import seaborn as sns
from io import StringIO
import os
import argparse
import base64
from io import BytesIO

# Create output directory if needed

def ensure_dir(directory):
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

# Enable high-quality output
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.style.use('ggplot')


def generate_analysis_report(data_csv, comparison_data=None, output_dir=None, return_images_as_b64=False):
    """
    Generate AI content analysis report with visualizations
    
    Parameters:
    -----------
    data_csv : str
        CSV data containing raw metrics. Can be:
        - A string containing CSV data
        - A path to a CSV file
        Required parameter - no sample data will be used
    
    comparison_data : str or None
        Markdown-formatted comparison data with deltas. Can be:
        - A string containing markdown data
        - A path to a markdown file
        If None, will be extracted from the CSV data
        
    output_dir : str or None
        Directory where output files will be saved
        If None, files will be saved in the current directory
        
    return_images_as_b64 : bool
        If True, returns images as base64 encoded strings
        Useful for AI systems to access the image data directly
        
    Returns:
    --------
    dict
        A dictionary containing:
        - 'markdown': The markdown report text
        - 'flow_diagram': The flow diagram (as base64 string if return_images_as_b64=True, otherwise path)
        - 'retention_matrix': The retention matrix chart (as base64 string if return_images_as_b64=True, otherwise path)
    
    Raises:
    -------
    ValueError
        If data_csv is None or empty
    """
    
    # Check if data is provided
    if not data_csv:
        raise ValueError("CSV data is required. Please provide CSV data as a string or file path.")
    
    # Set up output directory
    if output_dir:
        ensure_dir(output_dir)
    else:
        output_dir = "."
        
    # Handle file paths for input data
    if os.path.isfile(data_csv):
        with open(data_csv, 'r') as f:
            data_csv = f.read()
            
    if comparison_data and os.path.isfile(comparison_data):
        with open(comparison_data, 'r') as f:
            comparison_data = f.read()
    
    # Parse the CSV data
    try:
        df = pd.read_csv(StringIO(data_csv))
    except Exception as e:
        raise ValueError(f"Failed to parse CSV data: {str(e)}")
    
    # Auto-generate comparison data if not provided
    if comparison_data is None:
        comparison_data = auto_generate_comparison_data(df)
    
    # Parse the comparison data
    comp_sections = []
    current_section = None
    comp_lines = comparison_data.strip().split('\n')
    for line in comp_lines:
        if line.startswith('**'):
            if current_section:
                comp_sections.append(current_section)
            section_name = line.strip('*')
            current_section = {'name': section_name, 'data': []}
        elif ',' in line and not line.startswith('Comparison'):
            current_section['data'].append(line.split(','))
    if current_section:
        comp_sections.append(current_section)
    
    # Create a structured comparison dataframe
    comp_data = []
    for section in comp_sections:
        for row in section['data']:
            if len(row) >= 4:
                metric, high_b, base, delta = row
                comp_data.append({
                    'Section': section['name'],
                    'Metric': metric,
                    'High-B': float(high_b) if high_b and high_b != '–' else None,
                    'Base': float(base) if base and base != '–' else None,
                    'Delta': float(delta.replace('–', '-')) if delta and delta != '–' else 0
                })
    comp_df = pd.DataFrame(comp_data)
    
    # Extract the stages from section names
    stages = []
    for section in comp_sections:
        parts = section['name'].split(' vs ')
        if len(parts) == 2:
            if parts[0] not in stages:
                stages.append(parts[0])
            if parts[1] not in stages:
                stages.append(parts[1])
    
    # Reorder stages to show progression
    known_stages = ["Draft (AI)", "Refined (AI-assisted)", "Edited (Human-driven)", "Final (Human)"]
    stages = [stage for stage in known_stages if stage in stages or any(s in stage for s in stages)]
    
    # Map from the comparison data to known stages
    stage_mapping = {
        "Draft": "Draft (AI)",
        "Refined (AI-assisted)": "Refined (AI-assisted)",
        "Edited (Human-driven)": "Edited (Human-driven)",
        "Final (Human)": "Final (Human)"
    }
    
    # Create the markdown text output
    markdown_output = "# AI Content Transformation Analysis\n\n"
    
    # 1. Content Attribution Summary
    markdown_output += "## 1. Content Attribution Summary\n\n"
    
    # Calculate average alteration for each stage transition
    alt_metrics = {}
    for section in comp_sections:
        from_stage, to_stage = section['name'].split(' vs ')
        alt_data = [row for row in section['data'] if row[0] == 'Alteration %']
        if alt_data:
            alt_metrics[f"{from_stage} vs {to_stage}"] = float(alt_data[0][1])
    
    # Generate attribution summary
    markdown_output += "| Stage Transition | Human Contribution | AI Retention |\n"
    markdown_output += "|-----------------|-------------------|-------------|\n"
    
    for transition, alteration in alt_metrics.items():
        markdown_output += f"| {transition} | {alteration:.2f}% | {100-alteration:.2f}% |\n"
    
    # 2. Disclosure Recommendation
    markdown_output += "\n## 2. Disclosure Recommendation\n\n"
    
    # Find the overall alteration from AI to final
    try:
        draft_to_final_alt = max([v for k, v in alt_metrics.items() if 'Final' in k and 'Draft' in k], default=None)
        if draft_to_final_alt is None:
            # Estimate using stage transitions
            draft_to_final_alt = sum(alt_metrics.values()) / len(alt_metrics)
    except:
        draft_to_final_alt = 90  # Default if calculation fails
    
    # Generate recommended disclosure based on alteration level
    if draft_to_final_alt > 95:
        contribution_level = "minimal AI content"
    elif 80 <= draft_to_final_alt <= 95:
        contribution_level = "limited AI assistance"
    elif 50 <= draft_to_final_alt < 80:
        contribution_level = "significant human editing of AI content"
    else:
        contribution_level = "substantial AI contribution with human oversight"
    
    # Extract retention metrics
    char_retention = None
    word_retention = None
    for section in comp_sections:
        if "Final" in section['name'] and ("Draft" in section['name'] or "AI" in section['name']):
            for row in section['data']:
                if row[0] == 'Char Retention %':
                    char_retention = float(row[1])
                elif row[0] == 'Word Retention %':
                    word_retention = float(row[1])
    
    if char_retention is None:
        # Estimate from available data
        char_retention_values = [float(row[1]) for section in comp_sections for row in section['data'] if row[0] == 'Char Retention %']
        char_retention = min(char_retention_values) if char_retention_values else 10
    
    if word_retention is None:
        # Estimate from available data
        word_retention_values = [float(row[1]) for section in comp_sections for row in section['data'] if row[0] == 'Word Retention %']
        word_retention = min(word_retention_values) if word_retention_values else 25
    
    markdown_output += f"""```
AI Assistance Disclosure: This article utilized AI tools for {contribution_level}. 
The final published version contains approximately {char_retention:.2f}% character 
retention and {word_retention:.2f}% word retention from the initial AI draft. 
All factual information, analyses, and conclusions have been verified by 
human editors who take full responsibility for the content.
```\n"""
    
    # 3. Transformation Data Table
    markdown_output += "\n## 3. Transformation Data by Stage\n\n"
    
    # Extract metrics for each stage transition
    for section in comp_sections:
        markdown_output += f"### {section['name']}\n\n"
        markdown_output += "| Metric | High-B | Base | Delta |\n"
        markdown_output += "|--------|--------|------|-------|\n"
        
        for row in section['data']:
            metric, high_b, base, delta = row
            # Format delta with +/- sign
            if delta and delta != '0':
                delta_formatted = delta if delta.startswith('–') else f"+{delta}"
            else:
                delta_formatted = delta
            
            markdown_output += f"| {metric} | {high_b} | {base} | {delta_formatted} |\n"
        
        markdown_output += "\n"
    
    # Print the markdown output
    print(markdown_output)
    
    # Define output paths
    flow_diagram_path = os.path.join(output_dir, 'content_flow_diagram.png')
    retention_matrix_path = os.path.join(output_dir, 'retention_matrix_chart.png')
    
    # Create visualizations
    flow_fig = create_content_flow_diagram(comp_sections, stages, output_path=flow_diagram_path)
    retention_fig = create_retention_matrix_chart(comp_sections, stages, output_path=retention_matrix_path)
    
    # Prepare return values
    result = {
        'markdown': markdown_output,
        'flow_diagram': flow_diagram_path,
        'retention_matrix': retention_matrix_path
    }
    
    # Convert images to base64 if requested
    if return_images_as_b64:
        # Convert flow diagram to base64
        flow_buffer = BytesIO()
        flow_fig.savefig(flow_buffer, format='png', bbox_inches='tight', dpi=300)
        flow_buffer.seek(0)
        flow_b64 = base64.b64encode(flow_buffer.read()).decode('utf-8')
        result['flow_diagram'] = flow_b64
        
        # Convert retention matrix to base64
        retention_buffer = BytesIO()
        retention_fig.savefig(retention_buffer, format='png', bbox_inches='tight', dpi=300)
        retention_buffer.seek(0)
        retention_b64 = base64.b64encode(retention_buffer.read()).decode('utf-8')
        result['retention_matrix'] = retention_b64
    
    # Close figures to free memory
    plt.close(flow_fig)
    plt.close(retention_fig)
    
    return result


def create_content_flow_diagram(comp_sections, stages, output_path=None):
    """
    This function is replaced by create_alteration_pie_chart
    Kept for backward compatibility
    """
    return create_alteration_pie_chart(comp_sections, stages, output_path)


def create_retention_matrix_chart(comp_sections, stages, output_path=None):
    """
    Create a horizontal bar chart showing retention percentages by type
    
    Parameters:
    -----------
    comp_sections : list
        List of comparison section data
    stages : list
        List of content stages
    output_path : str or None
        Path to save the output image
        
    Returns:
    --------
    matplotlib.figure.Figure
        The figure object
        
    Raises:
    -------
    ValueError
        If insufficient data is available to create the chart
    """
    
    # Prepare data structure for retention metrics only (no alteration)
    metrics = ['Char Retention %', 'Word Retention %', 'Sentence Retention %', 'Paragraph Retention %']
    data = {metric: [] for metric in metrics}
    transitions = []
    
    # Extract data for each stage transition
    for i in range(len(stages) - 1):
        from_stage = stages[i]
        to_stage = stages[i+1]
        transition_label = f"{from_stage.split(' ')[0]} → {to_stage.split(' ')[0]}"
        
        # Find metrics for this transition
        metrics_found = False
        for section in comp_sections:
            if all(s in section['name'] for s in [from_stage.split(' ')[0], to_stage.split(' ')[0]]):
                transitions.append(transition_label)
                
                # Extract values for each metric
                for metric in metrics:
                    value = None
                    for row in section['data']:
                        if row[0] == metric:
                            try:
                                value = float(row[1])
                            except (ValueError, TypeError):
                                value = None
                            break
                    
                    if value is not None:
                        data[metric].append(value)
                    else:
                        data[metric].append(None)
                
                metrics_found = True
                break
    
    # Check if we have enough data
    has_valid_data = False
    for metric in metrics:
        if any(v is not None for v in data[metric]):
            has_valid_data = True
            break
            
    if not has_valid_data or not transitions:
        raise ValueError("Insufficient retention data available to create chart. Please provide retention percentages in the input data.")
    
    # Replace any None values with zeros to prevent plotting errors
    for metric in metrics:
        data[metric] = [0 if v is None else v for v in data[metric]]
    
    # Create the figure - horizontal orientation
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Set WCAG AA compliant color palette
    # These colors have been verified for sufficient contrast
    retention_colors = [
        '#0072B2',  # Blue
        '#009E73',  # Green
        '#D55E00',  # Orange
        '#CC79A7'   # Pink
    ]
    
    # Plot retention metrics as horizontal bars
    bar_height = 0.15
    y = np.arange(len(transitions))
    
    for i, metric in enumerate(metrics):
        ax.barh(y + (i - 1.5) * bar_height, data[metric], 
                height=bar_height, label=metric, color=retention_colors[i], alpha=0.85)
    
    # Configure axes
    ax.set_ylabel('Content Transformation Stages', fontsize=12)
    ax.set_xlabel('Retention Percentage (%)', fontsize=12)
    ax.set_yticks(y)
    ax.set_yticklabels(transitions)
    ax.set_xlim(0, 100)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Add legend
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=4, frameon=True, fontsize=11)
    
    # Add data labels on bars
    for i, metric in enumerate(metrics):
        for j, value in enumerate(data[metric]):
            if value > 0:  # Only add labels for non-zero values
                ax.text(value + 2, j + (i - 1.5) * bar_height, f"{value:.1f}%", 
                      va='center', fontsize=9, fontweight='bold')
    
    # Add title
    plt.title('Content Retention by Transformation Stage', fontsize=16, pad=20)
    
    plt.tight_layout()
    
    # Save the figure if path is provided
    if output_path:
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
    
    return fig


# Command line interface for easy usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AI Content Analysis Visualization Tool')
    parser.add_argument('--csv_data', type=str, required=True, 
                        help='Path to CSV data file or CSV data string (REQUIRED)')
    parser.add_argument('--output_dir', type=str, default='.', 
                        help='Directory to save output files')
    parser.add_argument('--b64_output', action='store_true', 
                        help='Return images as base64 strings (for AI use)')
    parser.add_argument('--save_report', action='store_true', 
                        help='Save markdown report to file')
    args = parser.parse_args()
    
    try:
        # Run the analysis
        result = generate_analysis_report(
            data_csv=args.csv_data,
            output_dir=args.output_dir,
            return_images_as_b64=args.b64_output
        )
        
        # Print the markdown report
        print(result['markdown'])
        
        # Save report to file if requested
        if args.save_report:
            report_path = os.path.join(args.output_dir, 'ai_content_analysis_report.md')
            with open(report_path, 'w') as f:
                f.write(result['markdown'])
            print(f"\nReport saved to: {report_path}")
            
        # Print paths to the generated images
        if not args.b64_output:
            print("\nVisualizations saved to:")
            if result['alteration_pie']:
                print(f"- Alteration Pie Chart: {result['alteration_pie']}")
            else:
                print("- Alteration Pie Chart: Could not be generated (insufficient data)")
                
            if result['retention_chart']:
                print(f"- Retention Bar Chart: {result['retention_chart']}")
            else:
                print("- Retention Bar Chart: Could not be generated (insufficient data)")
                
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nPlease provide a valid CSV file with the following structure:")
        print("Comparison,Metric,High-B,Base,Delta")
        print("\nExample row:")
        print("'Final (Human) vs Edited (Human-driven)',Char Retention %,68.43,68.43,0")
        print("\nExample usage:")
        print("python ai_content_analysis.py --csv_data path/to/data.csv --output_dir ./outputs")