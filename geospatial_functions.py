import pandas as pd, numpy as np
import geopandas as gpd
from shapely import wkt
import shapely as sp
from shapely.geometry import Point, LineString, Polygon


def find_interactions(geom_set1_df, geom_set2_df,
                      set1_key_cols, set2_key_cols,
                      set1_geometry_col, set2_geometry_col
                      ):

    set1_working_cols = set1_key_cols + [set1_geometry_col]
    set2_working_cols = set2_key_cols + [set2_geometry_col]
    
    # Convert point data to geopandas dataframe

    gdf1 = geom_set1_df[set1_working_cols]
    gdf1[set1_geometry_col] = gpd.GeoSeries.from_wkt(gdf1[set1_geometry_col])
    gdf1 = gpd.GeoDataFrame(gdf1, geometry=set1_geometry_col)

    # Add CRS (start with WGS84 to match lat/lon values)
    gdf1.set_crs(epsg=4326, inplace=True)
    gdf1_type = gdf1.loc[0, set1_geometry_col].geom_type

    #Convert polygon data to geopandas dataframe
    gdf2 = geom_set2_df[set2_working_cols]
    gdf2[set2_geometry_col] = gpd.GeoSeries.from_wkt(gdf2[set2_geometry_col])
    gdf2 = gpd.GeoDataFrame(gdf2, geometry=set2_geometry_col)

    # Add CRS (start with WGS84 to match lat/lon values)
    gdf2.set_crs(epsg=4326, inplace=True)

    gdf2_type = gdf2.loc[0, set2_geometry_col].geom_type

    #If datasets are mixed (one polygon and one linestring), ensure polygons are gdf1
    if (gdf1_type == 'LineString' or gdf1_type == 'Point') and gdf2_type == 'Polygon':
        gdf_temp = gdf1
        gdf1 = gdf2
        gdf2 = gdf_temp
        gdf2_type = gdf1_type
        gdf1_type = 'Polygon'
        keys_temp = set1_key_cols
        set1_key_cols = set2_key_cols
        set2_key_cols = keys_temp
        geom_temp = set1_geometry_col
        set1_geometry_col = set2_geometry_col
        set2_geometry_col = geom_temp
        
    # Convert to new equidistant projection

    #Prepare projection (North America Lambert Conformal Conic)
    # This projection is equidistant for measuring between points.
    # Units are in meters
    projout = '+proj=lcc +lat_1=20 +lat_2=60 +lat_0=40 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m no_defs'

    # Convert to Lambert projection
    gdf1 = gdf1.to_crs(projout)

    # Convert to Lambert projection
    gdf2 = gdf2.to_crs(projout)

#    if gdf2_type == 'Point':
#        results = pd.DataFrame(columns=(set1_key_cols + ['Within_polygon']))
#    else:
    results = pd.DataFrame(columns=(set1_key_cols + set2_key_cols + ['Interaction']))
    
    df_index = 0
    
# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
    for gdf1_index,gdf1_row in gdf1.iterrows():
        for gdf2_index,gdf2_row in gdf2.iterrows():
            if gdf1_type == 'Polygon' and gdf2_type == 'LineString':
                interaction = gdf1.loc[gdf1_index, set1_geometry_col].intersects(gdf2.loc[gdf2_index, set2_geometry_col])
                if interaction:
                    start_pt, end_pt = gdf2.loc[gdf2_index, set2_geometry_col].boundary
                    if gdf1.loc[gdf1_index, set1_geometry_col].contains(gdf2.loc[gdf2_index, set2_geometry_col]):
                        interact_str = ['Contains']
                    elif gdf1.loc[gdf1_index, set1_geometry_col].contains(start_pt):
                        interact_str = ['Start']
                    elif gdf1.loc[gdf1_index, set1_geometry_col].contains(end_pt):
                        interact_str = ['End']
                    else:
                        interact_str = ['Intersect']

                    results.loc[df_index] = np.concatenate((gdf1.loc[gdf1_index, set1_key_cols].values,
                                            gdf2.loc[gdf2_index, set2_key_cols].values,
                                            interact_str),axis=None)
                    df_index += 1
            elif gdf1_type == 'LineString' and gdf2_type == 'LineString':
                interaction = gdf1.loc[gdf1_index, set1_geometry_col].intersects(gdf2.loc[gdf2_index, set2_geometry_col])
                if interaction:
                    interact_str = ['Intersect']

                    results.loc[df_index] = np.concatenate((gdf1.loc[gdf1_index, set1_key_cols].values,
                                            gdf2.loc[gdf2_index, set2_key_cols].values,
                                            interact_str),axis=None)
                    df_index += 1
            elif gdf1_type == 'Polygon' and gdf2_type == 'Polygon':
                interaction = gdf1.loc[gdf1_index, set1_geometry_col].intersects(gdf2.loc[gdf2_index, set2_geometry_col])
                if interaction:
                    if gdf1.loc[gdf1_index, set1_geometry_col].contains(gdf2.loc[gdf2_index, set2_geometry_col]):
                        interact_str = ['Contains']
                    else:
                        interact_str = ['Intersect']

                    results.loc[df_index] = np.concatenate((gdf1.loc[gdf1_index, set1_key_cols].values,
                                            gdf2.loc[gdf2_index, set2_key_cols].values,
                                            interact_str),axis=None)
                    df_index += 1
            elif gdf1_type == 'Polygon' and gdf2_type == 'Point':            
                if gdf2.loc[gdf2_index, set2_geometry_col].within(gdf1.loc[gdf1_index, set1_geometry_col]):
                    results.loc[df_index] = np.concatenate((gdf1.loc[gdf1_index, set1_key_cols].values,
                                                            gdf2.loc[gdf2_index, set2_key_cols].values,
                                                            "Contained"),axis=None)
                    df_index += 1

            else:
                print('no match')
                
                
    return results


def conv_dist(distance_value, units_value):
    # Determine the conversion factor for the specified units (meters are required for this projection)
    if units_value == "mi":
        unit_factor = 1609.344
    elif units_value == "km":
        unit_factor = 1000.0
    elif units_value == "ft":
        unit_factor = 0.3048
    elif units_value == "nm":
        unit_factor = 1852
    elif units_value == "m":
        unit_factor = 1
    else:  # Bad units
        unit_factor = 0

    return distance_value * unit_factor


def gen_geocircle(input_df, key_col, center_col, radius_col, units_col):

    # Convert point data to geopandas dataframe
#    pointsdf = input_df[[key_col, center_col, radius_col, units_col]]

    working_cols = [key_col] + [center_col] + [radius_col] + [units_col]
    return_cols = [key_col] + ["buffer"]
    
    pointsdf = input_df[working_cols]
    
    pointsdf[center_col] = gpd.GeoSeries.from_wkt(pointsdf[center_col])
    gdf_pts = gpd.GeoDataFrame(pointsdf, geometry=center_col)

    # Add CRS (start with WGS84 to match lat/lon values)
    gdf_pts.set_crs(epsg=4326, inplace=True)

    #Prepare projection (North America Lambert Conformal Conic)
    # This projection is equidistant for measuring between points.
    # Units are in meters
    projout = '+proj=lcc +lat_1=20 +lat_2=60 +lat_0=40 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m no_defs'

    # Convert to Lambert projection
    gdf_pts = gdf_pts.to_crs(projout)

    # -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
    gdf_pts[units_col] = gdf_pts[units_col].str.lower()
    gdf_pts["dist"] = 0

    # -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
    for pt_index,pt_row in gdf_pts.iterrows():
        dvalue = conv_dist(pt_row[2], pt_row[3])

        gdf_pts.loc[pt_index,'dist'] = dvalue

#    gdf2 = pd.merge(gdf_pts[["locid","ArptLocation"]], params[["locid","dist"]], on='locid')

    gdf_pts["buffer"] = gdf_pts[center_col].buffer(gdf_pts['dist'])

    # -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
    gdf_circle = gdf_pts[return_cols]

    gdf_circle = gpd.GeoDataFrame(gdf_circle, geometry='buffer')

    gdf_circle = gdf_circle.to_crs(epsg=4326)

    
    return gdf_circle


def pt_poly_interactions(input_point_df, input_polygon_df, 
                         point_key_col, polygon_key_col, 
                         point_geometry_col, polygon_geometry_col):

    # Convert point data to geopandas dataframe
    pts_working_cols = point_key_col + [point_geometry_col]

    pointsdf = input_point_df[pts_working_cols]
    pointsdf[point_geometry_col] = gpd.GeoSeries.from_wkt(pointsdf[point_geometry_col])
    gdf_pts = gpd.GeoDataFrame(pointsdf, geometry=point_geometry_col)

    # Add CRS (start with WGS84 to match lat/lon values)
    gdf_pts.set_crs(epsg=4326, inplace=True)

    # -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
    #Convert polygon data to geopandas dataframe
    polys_working_cols = [polygon_key_col] + [polygon_geometry_col]

    polysdf = input_polygon_df[polys_working_cols]
    polysdf[polygon_geometry_col] = gpd.GeoSeries.from_wkt(polysdf[polygon_geometry_col])
    gdf_polys = gpd.GeoDataFrame(polysdf, geometry=polygon_geometry_col)

    # Add CRS (start with WGS84 to match lat/lon values)
    gdf_polys.set_crs(epsg=4326, inplace=True)

    # -------------------------------------------------------------------------------- NOTEBOOK-CELL: MARKDOWN
    # # Convert to new equidistant projection

    # -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
    #Prepare projection (North America Lambert Conformal Conic)
    # This projection is equidistant for measuring between points.
    # Units are in meters
    projout = '+proj=lcc +lat_1=20 +lat_2=60 +lat_0=40 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m no_defs'

    # Convert to Lambert projection
    gdf_pts = gdf_pts.to_crs(projout)

    # Convert to Lambert projection
    gdf_polys = gdf_polys.to_crs(projout)

    #gdf_pts.crs

    #gdf_polys.crs

    # -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
    gdf_polys = pd.concat([gdf_polys, gdf_polys.centroid], axis=1)
    gdf_polys.columns = polys_working_cols + ['Centroid']
    
    # -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
    #gdf_polys

    # -------------------------------------------------------------------------------- NOTEBOOK-CELL: MARKDOWN
    # # Make polygon assignments and calculate distance from centroid

    # -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
    # Add column to hold the polygon name
    gdf_pts["within_poly"] = ""
    gdf_pts["distance_from_centroid"] = 0.0

    # -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
    for poly_index,poly_row in gdf_polys.iterrows():
        for pt_index,pt_row in gdf_pts.iterrows():
            if pt_row[2] == "" and pt_row[1].within(poly_row[1]):
                gdf_pts.loc[pt_index, 'within_poly'] = poly_row[0]
                new_point = pt_row[point_geometry_col]
                distance = poly_row['Centroid'].distance(new_point)
                # Convert distance from meters to miles
                distance /= 1609.344
                gdf_pts.loc[pt_index, 'distance_from_centroid'] = distance

    # -------------------------------------------------------------------------------- NOTEBOOK-CELL: MARKDOWN
    # # Convert back to WGS84 projection

    # -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
    gdf_pts = gdf_pts.to_crs(epsg=4326)

    # -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
    return gdf_pts # Compute a Pandas dataframe to return
    

def gen_polygon(input_df, key_col, extra_col, x_col, y_col):

    # Extract the general, non-geometry fields for each flight
    keep_col = key_col + extra_col
    output_df = input_df[keep_col]

    # Remove duplicates (goal is one record per flight)
    output_df = output_df.drop_duplicates()
    
    # Sort and reset index
#    output_df = output_df.sort_values(by = key_col, ignore_index = True)
    output_df = output_df.sort_values(by = key_col)
    output_df = output_df.reset_index(drop=True)
 
    # Generate geopoints from input
    input_pts = input_df[[x_col, y_col]]
    geom2d = [Point(xy) for xy in zip(input_pts[x_col], input_pts[y_col])]
    input_df = gpd.GeoDataFrame(input_df, geometry=geom2d)

    # Generate linestrings from geopoints for each input object
    df3 = input_df.groupby(key_col)['geometry'].apply(lambda x: Polygon(x.tolist()) if x.size > 1 else x.tolist())

    # Reset indexes and relabel columns for concatenation with data columns
    df3 = pd.DataFrame(df3)
    df3 = df3.reset_index()
    new_col_names = []
    for col in key_col:
            new_col_names.append(col)
    df3.columns = new_col_names + ['boundary']

    # Concatenate flight information with linestring column
    output_df = pd.merge(output_df, df3, on=key_col)
    
    # Remove duplicate rows.  Note this step can be temporarily disabled for troubleshooting
 #   output_df = output_df.drop(columns = new_col_names)
    
    return output_df
	

def gen_linestring(input_df, key_col, sort_col, extra_col, x_col, y_col, z_col, t_col):

    # Extract the general, non-geometry fields for each flight
    keep_col = key_col + extra_col
    output_df = input_df[keep_col]

    # Remove duplicates (goal is one record per flight)
    output_df = output_df.drop_duplicates()
    
    # Sort and reset index
#    output_df = output_df.sort_values(by = key_col, ignore_index = True)
    output_df = output_df.sort_values(by = key_col)
    output_df = output_df.reset_index(drop=True)
 
    # Generate geopoints from input
    if z_col == 'None':
        input_pts = input_df[[x_col, y_col]]
        geom2d = [Point(xy) for xy in zip(input_pts[x_col], input_pts[y_col])]
        input_df = gpd.GeoDataFrame(input_df, geometry=geom2d)
    else:
        input_pts = input_df[[x_col, y_col, z_col]]
        geom3d = [Point(xyz) for xyz in zip(input_pts[x_col], input_pts[y_col], input_pts[z_col])]
        input_df = gpd.GeoDataFrame(input_df, geometry=geom3d)

    # Generate linestrings from geopoints for each input object
    df3 = input_df.groupby(key_col)['geometry'].apply(lambda x: LineString(x.tolist()) if x.size > 1 else x.tolist())

    # Reset indexes and relabel columns for concatenation with data columns
    df3 = df3.reset_index()
    new_col_names = []
    for col in key_col:
            new_col_names.append(col)
    if z_col == 'None':
        df3.columns = new_col_names + ['geom2d']
    else:
        df3.columns = new_col_names + ['geom3d']

    # Concatenate flight information with linestring column
    output_df = pd.merge(output_df, df3, on=key_col)
    
    if t_col != 'None':
        tempdf1 = input_df[key_col + [t_col]]

        fdict = {}
        old_key= []
        for x_index, x_row in tempdf1.iterrows():
            new_key = tuple([x_row[key] for key in key_col])
            datestr = x_row[t_col].isoformat().replace("+00:00","Z") + "Z"

            if old_key != new_key:
#                fdict[new_key] = [str(x_row[t_col])]
                fdict[new_key] = [datestr]
                old_key = new_key
            else:
                fdict[new_key].append(datestr)
#                fdict[new_key].append(str(x_row[t_col]))

        new_col_list = []

        for x_ind, x_row in output_df.iterrows():

            d_key = tuple([x_row[key] for key in key_col])
            cur_timestamps = fdict[d_key]

            new_col_list.append(tuple(cur_timestamps))

        output_df['positiontimes'] = new_col_list

        # Remove duplicate rows.  Note this step can be temporarily disabled for troubleshooting
 #   output_df = output_df.drop(columns = new_col_names)
    
    return output_df