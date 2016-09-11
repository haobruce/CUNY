library(hash)

# read UCI data into dataframe
df = read.csv("https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data", header=FALSE)
# manually add column names
colnames(df) = c('classes','cap_shape','cap_surface','cap_color','bruises?','odor','gill_attachment','gill_spacing',
  'gill_size','gill_color','stalk_shape','stalk_root','stalk_surface_above_ring','stalk_surface_below_ring',
  'stalk_color_above_ring','stalk_color_below_ring','veil_type','veil_color','ring_number','ring_type','spore_print_color',
  'population','habitat')
# create hash tables for abbreviations within each column
classes = hash(keys=c('e','p'), 
                 values=c('edible','poisonous'))
cap_shape = hash(keys=c('b','c','x','f','k','s'), 
                 values=c('bell','conical','convex','flat','knobbed','sunken'))
cap_surface = hash(keys=c('f','g','y','s'), 
               values=c('fibrous','grooves','scaly','smooth'))
cap_color = hash(keys=c('n','b','c','g','r','p','u','e','w','y'), 
               values=c('brown','buff','cinnamon','gray','green','pink','purple','red','white','yellow'))

# loop through whichever columns and rename data
# the better approach would be to programmatically change the factor names using levels(df...), 
# but need to learn how to use apply
for (i in 1:4) {
  for (key in as.list(keys(get(columnName)))) {
    levels(df[[columnName]]) = c(levels(df[[columnName]]), get(columnName)[[key]])
    df[df[columnName]==key, columnName] = get(columnName)[[key]]
  }
}
