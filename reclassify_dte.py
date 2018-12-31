import subprocess
from pathlib import Path

class ReclassifyDTE:
	"""Class to classify continuous DTE rasters to binary"""

	def __init__(self, iso, BASEDIR, DATAIN, OUTDIR):
		"""Initialisation"""
		self.iso = iso
		self.BASEDIR = BASEDIR
		self.DATAIN = DATAIN
		self.OUTDIR = OUTDIR
		self.make_out_folders()
		self.rasters = self.list_rasters()
		self.reclassify(self.rasters)

	def make_out_folders(self):
		"""Make folders in which to hold output if none exist"""
		if not self.OUTDIR.exists():
			self.OUTDIR.mkdir(parents=True)

	def list_rasters(self):
		"""Make a list of rasters to reclassify"""
		return [x for x in self.DATAIN.iterdir()]

	def reclassify(self, rasters):
		"""Loops over rasters and reclassifies to binary"""
		for raster in rasters:
			outraster = self.OUTDIR.joinpath('{0}_DTE_bin_{1}'.format(self.iso, str(raster)[-8:]))
			gdal_command = "gdal_calc.py -A {0} --outfile={1} --calc='1 * (A<=0) + 0 * (A>0)' --NoDataValue=255 --type=Byte --co=COMPRESS=LZW --co PREDICTOR=2 --co BIGTIFF=YES".format(str(raster), str(outraster))
			subprocess.call(gdal_command, shell=True)



if __name__ == "__main__":
	isos = ['CHE']
	for iso in isos:
		BASEDIR = Path(__file__).resolve().parent.parent
		DATAIN = BASEDIR.joinpath('datain', iso)
		OUTDIR = BASEDIR.joinpath('output', iso)
		x = ReclassifyDTE(iso, BASEDIR, DATAIN, OUTDIR)
		